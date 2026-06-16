import asyncio
import json
import os
import time
from typing import Dict, List, Tuple

from agent.main_agent import MainAgent
from engine.llm_judge import LLMJudge
from engine.retrieval_eval import RetrievalEvaluator
from engine.runner import BenchmarkRunner


def load_dataset(path: str = "data/golden_set.jsonl") -> List[Dict]:
    if not os.path.exists(path):
        raise FileNotFoundError("Missing data/golden_set.jsonl. Run: python data/synthetic_gen.py")

    with open(path, "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f if line.strip()]

    if len(dataset) < 50:
        raise ValueError(f"Golden dataset must contain at least 50 cases; found {len(dataset)}")

    required = {"id", "question", "expected_answer", "expected_retrieval_ids", "metadata"}
    for case in dataset:
        missing = required - set(case)
        if missing:
            raise ValueError(f"Case {case.get('id', '<unknown>')} missing fields: {sorted(missing)}")

    return dataset


def summarize_results(agent_version: str, results: List[Dict], started_at: float) -> Dict:
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "pass")
    failed = sum(1 for r in results if r["status"] == "fail")
    errors = sum(1 for r in results if r["status"] == "error")
    retrieval_cases = [r for r in results if r.get("expected_retrieval_ids")]
    retrieval_denominator = len(retrieval_cases) or 1

    total_tokens = sum(r.get("metadata", {}).get("agent", {}).get("tokens_used", 0) for r in results)
    total_cost = sum(r.get("metadata", {}).get("agent", {}).get("estimated_cost_usd", 0.0) for r in results)

    by_type: Dict[str, Dict[str, float]] = {}
    for result in results:
        case_type = result.get("metadata", {}).get("type", "unknown")
        bucket = by_type.setdefault(case_type, {"count": 0, "score_sum": 0.0, "fails": 0})
        bucket["count"] += 1
        bucket["score_sum"] += result["judge"]["final_score"]
        if result["status"] != "pass":
            bucket["fails"] += 1

    for bucket in by_type.values():
        bucket["avg_score"] = round(bucket["score_sum"] / bucket["count"], 4)
        bucket["fail_rate"] = round(bucket["fails"] / bucket["count"], 4)
        del bucket["score_sum"]

    return {
        "metadata": {
            "version": agent_version,
            "total": total,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_seconds": round(time.perf_counter() - started_at, 4),
            "judge_models": ["coverage_judge", "policy_judge"],
        },
        "metrics": {
            "avg_score": round(sum(r["judge"]["final_score"] for r in results) / total, 4),
            "pass_rate": round(passed / total, 4),
            "fail_count": failed,
            "error_count": errors,
            "hit_rate": round(
                sum(r["ragas"]["retrieval"]["hit_rate"] for r in retrieval_cases) / retrieval_denominator,
                4,
            ),
            "mrr": round(
                sum(r["ragas"]["retrieval"]["mrr"] for r in retrieval_cases) / retrieval_denominator,
                4,
            ),
            "faithfulness": round(sum(r["ragas"]["faithfulness"] for r in results) / total, 4),
            "relevancy": round(sum(r["ragas"]["relevancy"] for r in results) / total, 4),
            "agreement_rate": round(sum(r["judge"]["agreement_rate"] for r in results) / total, 4),
            "avg_latency_seconds": round(sum(r["latency"] for r in results) / total, 4),
            "total_tokens": total_tokens,
            "estimated_cost_usd": round(total_cost, 6),
            "cost_per_case_usd": round(total_cost / total, 6),
        },
        "breakdown_by_type": by_type,
    }


async def run_benchmark_with_results(agent_version: str, dataset: List[Dict]) -> Tuple[List[Dict], Dict]:
    print(f"Starting benchmark for {agent_version}...")
    started_at = time.perf_counter()
    runner = BenchmarkRunner(MainAgent(version=agent_version), RetrievalEvaluator(), LLMJudge())
    results = await runner.run_all(dataset)
    summary = summarize_results(agent_version, results, started_at)
    return results, summary


def evaluate_release_gate(v1_summary: Dict, v2_summary: Dict) -> Dict:
    v1 = v1_summary["metrics"]
    v2 = v2_summary["metrics"]
    delta_score = round(v2["avg_score"] - v1["avg_score"], 4)
    delta_hit_rate = round(v2["hit_rate"] - v1["hit_rate"], 4)
    delta_latency = round(v2["avg_latency_seconds"] - v1["avg_latency_seconds"], 4)
    delta_cost = round(v2["cost_per_case_usd"] - v1["cost_per_case_usd"], 6)

    checks = {
        "quality_not_regressed": delta_score >= -0.05,
        "retrieval_not_regressed": delta_hit_rate >= -0.02,
        "minimum_avg_score": v2["avg_score"] >= 3.5,
        "minimum_hit_rate": v2["hit_rate"] >= 0.85,
        "agreement_acceptable": v2["agreement_rate"] >= 0.65,
        "latency_acceptable": v2["avg_latency_seconds"] <= 0.2,
    }

    decision = "APPROVE" if all(checks.values()) and delta_score >= 0 else "BLOCK_RELEASE"

    return {
        "decision": decision,
        "checks": checks,
        "delta": {
            "avg_score": delta_score,
            "hit_rate": delta_hit_rate,
            "avg_latency_seconds": delta_latency,
            "cost_per_case_usd": delta_cost,
        },
        "baseline": {
            "version": v1_summary["metadata"]["version"],
            "metrics": v1,
        },
    }


async def main():
    try:
        dataset = load_dataset()
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return

    v1_results, v1_summary = await run_benchmark_with_results("v1", dataset)
    v2_results, v2_summary = await run_benchmark_with_results("v2", dataset)
    release_gate = evaluate_release_gate(v1_summary, v2_summary)
    v2_summary["regression"] = release_gate

    os.makedirs("reports", exist_ok=True)
    with open("reports/summary.json", "w", encoding="utf-8") as f:
        json.dump(v2_summary, f, ensure_ascii=False, indent=2)
    with open("reports/benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(v2_results, f, ensure_ascii=False, indent=2)
    with open("reports/regression_comparison.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "v1_summary": v1_summary,
                "v2_summary": v2_summary,
                "v1_results": v1_results,
                "release_gate": release_gate,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print("\n--- REGRESSION SUMMARY ---")
    print(f"V1 avg_score: {v1_summary['metrics']['avg_score']}")
    print(f"V2 avg_score: {v2_summary['metrics']['avg_score']}")
    print(f"Delta score: {release_gate['delta']['avg_score']:+.4f}")
    print(f"V2 hit_rate: {v2_summary['metrics']['hit_rate']}")
    print(f"V2 MRR: {v2_summary['metrics']['mrr']}")
    print(f"Decision: {release_gate['decision']}")
    print("Reports written to reports/")


if __name__ == "__main__":
    asyncio.run(main())
