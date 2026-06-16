import asyncio
import time
from typing import Dict, List


class BenchmarkRunner:
    def __init__(self, agent, evaluator, judge):
        self.agent = agent
        self.evaluator = evaluator
        self.judge = judge

    async def run_single_test(self, test_case: Dict) -> Dict:
        start_time = time.perf_counter()

        try:
            response = await self.agent.query(test_case["question"])
            latency = time.perf_counter() - start_time

            ragas_scores = await self.evaluator.score(test_case, response)
            judge_result = await self.judge.evaluate_multi_judge(
                test_case["question"],
                response["answer"],
                test_case["expected_answer"],
            )

            return {
                "id": test_case.get("id"),
                "test_case": test_case["question"],
                "expected_answer": test_case.get("expected_answer"),
                "expected_retrieval_ids": test_case.get("expected_retrieval_ids", []),
                "agent_response": response["answer"],
                "retrieved_ids": response.get("retrieved_ids", []),
                "latency": round(latency, 4),
                "ragas": ragas_scores,
                "judge": judge_result,
                "metadata": {
                    **test_case.get("metadata", {}),
                    "agent": response.get("metadata", {}),
                },
                "status": "fail" if judge_result["final_score"] < 3 else "pass",
            }
        except Exception as exc:
            latency = time.perf_counter() - start_time
            return {
                "id": test_case.get("id"),
                "test_case": test_case.get("question"),
                "latency": round(latency, 4),
                "status": "error",
                "error": str(exc),
                "ragas": {
                    "faithfulness": 0.0,
                    "relevancy": 0.0,
                    "answer_overlap": 0.0,
                    "retrieval": {
                        "hit_rate": 0.0,
                        "mrr": 0.0,
                        "expected_ids": test_case.get("expected_retrieval_ids", []),
                        "retrieved_ids": [],
                    },
                },
                "judge": {
                    "final_score": 0.0,
                    "agreement_rate": 0.0,
                    "individual_scores": {},
                    "conflict_resolution": "error",
                },
            }

    async def run_all(self, dataset: List[Dict], batch_size: int = 10) -> List[Dict]:
        results = []
        for i in range(0, len(dataset), batch_size):
            batch = dataset[i : i + batch_size]
            tasks = [self.run_single_test(case) for case in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
        return results
