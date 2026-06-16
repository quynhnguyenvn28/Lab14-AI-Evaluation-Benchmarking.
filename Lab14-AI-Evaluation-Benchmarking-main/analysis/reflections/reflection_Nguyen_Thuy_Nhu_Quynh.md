# Reflection ca nhan - Nguyen Thuy Nhu Quynh

- MSSV: 2A202600557
- Vai tro: Multi-judge, rubric va agreement

## Dong gop chinh

Toi phu trach xay dung evaluator gom hai judge doc lap: `coverage_judge` va `policy_judge`. Hai judge dung rubric khac nhau de giam rui ro chi phu thuoc vao mot cach cham diem.

Artifact lien quan:

- `engine/llm_judge.py`
- Truong `judge` trong `reports/benchmark_results.json`
- Metric `agreement_rate` trong `reports/summary.json`

## Giai thich ky thuat

`coverage_judge` cham muc do cau tra loi bao phu expected answer. `policy_judge` tap trung vao safety, refusal behavior, prompt-injection va policy-boundary.

Agreement rate duoc tinh dua tren do lech diem giua hai judge. Neu hai judge lech tren 1 diem, pipeline dung conflict resolution kieu conservative adjudication, nghia la final score nghieng ve diem thap hon de tranh approve nham cau tra loi co rui ro.

## Van de da gap

Judge heuristic co the khong hieu ngu nghia sau nhu LLM that. Vi vay rubric can duoc viet ro, output schema can on dinh va report can ghi ro day la offline judge. Khi co API key, co the thay hai judge bang GPT va Claude nhung giu nguyen contract `evaluate_multi_judge`.

## Bai hoc

Multi-judge khong chi la lay trung binh diem. Can do agreement, phat hien conflict va co logic xu ly khi judge bat dong, dac biet voi cac cau hoi safety hoac out-of-context.
