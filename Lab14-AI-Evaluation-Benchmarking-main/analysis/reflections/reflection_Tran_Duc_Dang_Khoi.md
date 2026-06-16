# Reflection ca nhan - Tran Duc Dang Khoi

- MSSV: 2A202600889
- Vai tro: Retrieval evaluation va benchmark runner

## Dong gop chinh

Trong bai lab nay, phan viec cua toi tap trung vao do luong chat luong retrieval truoc khi danh gia generation. Toi phu trach logic Hit Rate, MRR va ket noi cac metric nay vao pipeline benchmark bat dong bo.

Artifact lien quan:

- `engine/retrieval_eval.py`
- `engine/runner.py`
- Mot phan schema output trong `reports/benchmark_results.json`

## Giai thich ky thuat

Hit Rate tra loi cau hoi: trong top-k document ma retriever lay ra, co it nhat mot document dung hay khong. Metric nay phu hop de phat hien loi "khong tim thay nguon dung".

MRR do document dung xuat hien som den muc nao. Neu document dung o rank 1 thi MRR = 1.0; rank 2 thi MRR = 0.5. Trong benchmark cuoi, V2 dat Hit Rate 1.0 va MRR 0.9896, cho thay retriever khong chi lay duoc document dung ma con dua document dung len rat cao.

## Van de da gap

Baseline V1 hay sai voi query ngan nhu "vpn", "hoan tien", "nghi phep" vi chi dung token overlap. Cach xu ly la them keyword/category boost va ghi lai `retrieved_ids` trong response de co the debug tung case.

## Bai hoc

Neu chi cham answer ma bo qua retrieval, nhom se khong biet loi den tu retriever hay generator. Tach ro retrieval metrics giup viec debug nhanh va co bang chung dinh luong khi so sanh V1/V2.
