import json
import os


def validate_lab():
    print("Dang kiem tra dinh dang bai nop...")

    required_files = [
        "data/golden_set.jsonl",
        "reports/summary.json",
        "reports/benchmark_results.json",
        "analysis/failure_analysis.md",
        "analysis/reflections/reflection_Tran_Duc_Dang_Khoi.md",
        "analysis/reflections/reflection_Le_Thien_Khang.md",
        "analysis/reflections/reflection_Nguyen_Thuy_Nhu_Quynh.md",
        "analysis/reflections/reflection_Pham_Thanh_Nam.md",
    ]

    missing = []
    for path in required_files:
        if os.path.exists(path):
            print(f"OK: {path}")
        else:
            print(f"MISSING: {path}")
            missing.append(path)

    if missing:
        print(f"\nThieu {len(missing)} file. Hay bo sung truoc khi nop bai.")
        return

    try:
        with open("reports/summary.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        print(f"reports/summary.json khong phai JSON hop le: {exc}")
        return

    if "metrics" not in data or "metadata" not in data:
        print("summary.json thieu truong 'metrics' hoac 'metadata'.")
        return

    metrics = data["metrics"]
    print("\n--- Thong ke nhanh ---")
    print(f"Tong so cases: {data['metadata'].get('total', 'N/A')}")
    print(f"Diem trung binh: {metrics.get('avg_score', 0):.2f}")

    if "hit_rate" in metrics:
        print(f"OK: Retrieval Hit Rate = {metrics['hit_rate'] * 100:.1f}%")
    else:
        print("WARNING: Thieu Retrieval Metrics (hit_rate).")

    if "mrr" in metrics:
        print(f"OK: MRR = {metrics['mrr']:.4f}")
    else:
        print("WARNING: Thieu Retrieval Metrics (mrr).")

    if "agreement_rate" in metrics:
        print(f"OK: Multi-Judge Agreement Rate = {metrics['agreement_rate'] * 100:.1f}%")
    else:
        print("WARNING: Thieu Multi-Judge Metrics (agreement_rate).")

    if data["metadata"].get("version"):
        print("OK: Co thong tin phien ban Agent.")

    try:
        with open("data/golden_set.jsonl", "r", encoding="utf-8") as f:
            cases = [json.loads(line) for line in f if line.strip()]
    except json.JSONDecodeError as exc:
        print(f"data/golden_set.jsonl khong phai JSONL hop le: {exc}")
        return

    if len(cases) >= 50:
        print(f"OK: Golden Dataset co {len(cases)} cases.")
    else:
        print(f"WARNING: Golden Dataset chi co {len(cases)} cases, can it nhat 50.")

    required_case_fields = {"id", "question", "expected_answer", "expected_retrieval_ids", "metadata"}
    invalid_cases = [
        case.get("id", f"line_{index + 1}")
        for index, case in enumerate(cases)
        if not required_case_fields.issubset(case)
    ]
    if invalid_cases:
        print(f"WARNING: Co case thieu schema bat buoc: {invalid_cases[:5]}")
    else:
        print("OK: Golden Dataset co du schema bat buoc.")

    if "regression" in data and data["regression"].get("decision"):
        print(f"OK: Release Gate = {data['regression']['decision']}")

    print("\nBai lab da san sang de cham diem.")


if __name__ == "__main__":
    validate_lab()
