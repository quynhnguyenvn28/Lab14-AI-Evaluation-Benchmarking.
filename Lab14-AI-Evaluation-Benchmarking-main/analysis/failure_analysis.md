# Bao cao phan tich that bai - Lab 14 AI Evaluation Benchmarking

## 1. Tong quan benchmark

Benchmark duoc chay tren `data/golden_set.jsonl` gom 60 test cases, bao phu fact-check, scenario, summarization, prompt-injection, goal-hijacking, policy-boundary, negative-case, safety, out-of-context va ambiguous.

Ket qua ban toi uu `v2`:

- Tong so cases: 60
- Pass/Fail: 60/0
- Avg judge score: 4.83 / 5.0
- Pass rate: 100%
- Hit Rate: 1.0
- MRR: 0.9896
- Faithfulness: 1.0
- Relevancy: 0.6802
- Multi-judge agreement rate: 0.925
- Avg latency: 0.0731 giay/case
- Tong token uoc tinh: 9,579
- Chi phi uoc tinh: 0.002211 USD/lua chay
- Release gate: APPROVE

Ket qua baseline `v1`:

- Avg judge score: 3.3142 / 5.0
- Pass rate: 48.33%
- Fail count: 31
- Hit Rate: 0.8125
- MRR: 0.6979
- Faithfulness: 0.7215
- Avg latency: 0.1 giay/case

Delta `v2 - v1`:

- Avg score: +1.5158
- Hit Rate: +0.1875
- Avg latency: -0.0269 giay
- Cost/case: -0.000001 USD

## 2. Phan nhom loi

V2 khong con case fail theo threshold `final_score >= 3`. De phan tich nguyen nhan goc, nhom su dung baseline V1 lam doi tuong failure clustering.

| Nhom loi V1 | So luong | Nguyen nhan chinh | Cach V2 khac phuc |
|---|---:|---|---|
| Summarization retrieval sai | 9 | V1 chi dung token overlap, khong boost keyword/cum tu quan trong | V2 them keyword boost va rule cho entity/cum tu |
| Scenario retrieval sai | 9 | Query ngan nhu "vpn", "hoan tien", "nghi phep" khong du suc keo dung document len top 1 | V2 dung `keywords` trong corpus va category boost |
| Out-of-context hallucination | 6 | V1 luon chon document gan nhat, ke ca khi cau hoi nam ngoai knowledge base | V2 co out-of-scope detection va nguong tu choi |
| Ambiguous question | 6 | V1 tu suy doan tai lieu thay vi hoi lai | V2 nhan dien mau cau hoi mo ho va yeu cau lam ro |
| Prompt injection | 1 | V1 khong co guardrail khi nguoi dung yeu cau bo qua tai lieu | V2 them safety prefix va van tra loi theo context |

## 3. Phan tich 5 Whys

### Case A: `case_003` - summarization ve `tai khoan`

Symptom: V1 can tom tat van de lien quan den tai khoan nhung retrieve `doc_data_retention`, `doc_leave_policy`, `doc_account_lock`; expected la `doc_password_reset`.

1. Why 1: Cau hoi ngan va chi co keyword chung "tai khoan".
2. Why 2: Token overlap khong phan biet duoc "doi mat khau" voi cac tai lieu cung nhac den tai khoan/nguoi dung.
3. Why 3: Corpus V1 khong dung keyword metadata de tang trong so cho topic chinh.
4. Why 4: Retriever khong co phrase/entity boost cho cac cum nghiep vu quan trong.
5. Root cause: Retrieval scoring qua don gian, chi dua vao overlap token nen de sai top-1 voi truy van ngan.

Fix trong V2: dung keyword boost, category boost, va metadata `keywords` trong `data/corpus.py`.

### Case B: `case_049` den `case_054` - out-of-context

Symptom: V1 tra loi bang tai lieu noi bo cho cac cau hoi nhu bitcoin, co phieu, bong da, tong thong.

1. Why 1: Agent luon lay document co score cao nhat.
2. Why 2: Khong co nguong confidence toi thieu truoc khi generate.
3. Why 3: Khong co danh sach topic ngoai pham vi de chan nhanh.
4. Why 4: Rubric ban dau chua ep agent noi "khong tim thay thong tin" khi context khong co.
5. Root cause: Thieu refusal policy cho cau hoi ngoai knowledge base.

Fix trong V2: them `_is_known_out_of_scope`, threshold `best_score < 0.18`, va cau tra loi tu choi dua tren tai lieu.

### Case C: `case_055` den `case_060` - ambiguous questions

Symptom: V1 tra loi bang mot tai lieu bat ky cho cac cau hoi nhu "Toi muon doi cai do, lam sao?" hoac "Gui yeu cau o dau?"

1. Why 1: Cau hoi thieu object/chinh sach cu the.
2. Why 2: Retriever van co the match mot vai token chung.
3. Why 3: Agent khong co buoc phan loai intent truoc retrieval.
4. Why 4: Prompt/logic khong bat buoc hoi lai khi confidence ngu nghia thap.
5. Root cause: Pipeline thieu ambiguous-intent handling truoc khi generate.

Fix trong V2: them `_is_ambiguous` de tra loi yeu cau lam ro thay vi suy doan.

## 4. Danh gia multi-judge

Pipeline dung 2 judge heuristic doc lap:

- `coverage_judge`: do muc do bao phu ground truth bang lexical overlap.
- `policy_judge`: kiem tra safety, refusal, prompt-injection va policy-boundary.

Agreement rate V2 dat 0.925. Conflict resolution dang dung `adjudicator_weighted_conservative`: neu hai judge lech tren 1 diem, final score nghieng ve diem thap hon de giam false positive.

Luu y: day la offline judge de dam bao lab chay duoc khong can API key. Neu can dung model that, thay hai judge nay bang GPT/Claude trong `engine/llm_judge.py` nhung giu schema output hien tai.

## 5. Release gate

Release gate APPROVE vi tat ca check deu dat:

- Khong regression chat luong: true
- Khong regression retrieval: true
- Avg score >= 3.5: true
- Hit Rate >= 0.85: true
- Agreement Rate >= 0.65: true
- Avg latency <= 0.2 giay: true

## 6. Ke hoach cai tien tiep theo

- Thay local heuristic judge bang 2 model that, vi du GPT va Claude, khi co API key.
- Bo sung Cohen's Kappa ben canh agreement rate de do dong thuan chat hon.
- Them reranker cho cac query ngan co nhieu document cung topic.
- Luu confusion matrix theo category de theo doi regression sau moi lan sua corpus.
- Mo rong golden dataset len 100+ cases neu co tai lieu san pham that.

## 7. Phan cong nhom

| Thanh vien | MSSV | Phan viec chinh | Artifact lien quan |
|---|---|---|---|
| Tran Duc Dang Khoi | 2A202600889 | Retrieval evaluation, Hit Rate/MRR, ket noi metrics vao runner | `engine/retrieval_eval.py`, `engine/runner.py` |
| Le Thien Khang | 2A202600726 | Golden dataset, SDG, hard cases va corpus | `data/corpus.py`, `data/synthetic_gen.py`, `data/golden_set.jsonl` |
| Nguyen Thuy Nhu Quynh | 2A202600557 | Multi-judge, rubric, agreement va conflict resolution | `engine/llm_judge.py` |
| Pham Thanh Nam | 2A202600832 | Regression gate, summary reports, benchmark orchestration | `main.py`, `reports/summary.json`, `reports/regression_comparison.json` |
