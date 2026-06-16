# Reflection ca nhan - Le Thien Khang

- MSSV: 2A202600726
- Vai tro: Golden dataset, SDG va hard cases

## Dong gop chinh

Toi phu trach thiet ke corpus noi bo va script sinh golden dataset. Dataset cuoi gom 60 cases, bao gom fact-check, scenario, summarization, prompt-injection, goal-hijacking, policy-boundary, safety, out-of-context va ambiguous.

Artifact lien quan:

- `data/corpus.py`
- `data/synthetic_gen.py`
- `data/golden_set.jsonl`
- `data/HARD_CASES_GUIDE.md`

## Giai thich ky thuat

Moi test case co `question`, `expected_answer`, `expected_retrieval_ids`, `context` va `metadata`. Truong `expected_retrieval_ids` rat quan trong vi no cho phep tinh Hit Rate/MRR thay vi chi danh gia answer.

Hard cases duoc thiet ke de kiem tra cac loi thuc te:

- Prompt injection: yeu cau bo qua tai lieu.
- Out-of-context: hoi ve topic khong co trong corpus.
- Ambiguous: cau hoi thieu ngu canh.
- Policy-boundary: cau hoi nam sat ranh gioi quy dinh.

## Van de da gap

Neu case qua de, benchmark khong phan biet duoc Agent V1 va V2. Neu case qua mo ho, judge lai kho cham on dinh. Cach can bang la tao nhieu nhom difficulty va gan metadata ro rang de phan tich theo type.

## Bai hoc

Chat luong benchmark phu thuoc rat lon vao dataset. Dataset tot phai co ground truth, retrieval ids va nhieu dang failure mode, khong chi co cau hoi fact-check don gian.
