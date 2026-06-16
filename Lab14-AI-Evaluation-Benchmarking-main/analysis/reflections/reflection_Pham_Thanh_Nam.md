# Reflection ca nhan - Pham Thanh Nam

- MSSV: 2A202600832
- Vai tro: Regression gate, reports va benchmark orchestration

## Dong gop chinh

Toi phu trach orchestration trong `main.py`: load dataset, chay benchmark cho Agent V1/V2, tong hop metrics, tao report JSON va dua ra release decision tu dong.

Artifact lien quan:

- `main.py`
- `reports/summary.json`
- `reports/benchmark_results.json`
- `reports/regression_comparison.json`

## Giai thich ky thuat

Regression gate so sanh V2 voi V1 theo nhieu chieu:

- Avg score khong duoc regression.
- Hit Rate khong duoc regression.
- Avg score phai dat nguong 3.5.
- Hit Rate phai dat nguong 0.85.
- Agreement rate phai dat nguong 0.65.
- Latency trung binh phai duoi 0.2 giay/case.

Ket qua cuoi: V2 dat avg score 4.83, Hit Rate 1.0, MRR 0.9896 va release gate APPROVE.

## Van de da gap

Neu chi in ket qua ra console thi kho audit va kho nop bai. Vi vay pipeline can ghi report co schema on dinh de `check_lab.py` va nguoi cham co the doc lai duoc.

## Bai hoc

Release gate nen dua tren nhieu metric, khong chi avg score. Mot agent co diem answer cao nhung retrieval kem hoac latency qua cao van co the khong san sang release.
