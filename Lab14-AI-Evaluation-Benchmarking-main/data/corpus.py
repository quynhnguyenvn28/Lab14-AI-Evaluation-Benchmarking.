DOCUMENTS = [
    {
        "id": "doc_password_reset",
        "title": "Quy trinh doi mat khau",
        "category": "account",
        "keywords": ["mat khau", "password", "doi mat khau", "quen mat khau", "tai khoan"],
        "summary_answer": (
            "Nguoi dung co the doi mat khau trong Settings > Security > Change password. "
            "Mat khau moi toi thieu 12 ky tu, co chu hoa, chu thuong, so va ky tu dac biet. "
            "Neu quen mat khau, dung Forgot password va xac minh qua email cong ty."
        ),
        "text": (
            "Tai lieu tai khoan: De doi mat khau, mo Settings, chon Security, sau do chon Change password. "
            "Mat khau moi phai co toi thieu 12 ky tu, bao gom chu hoa, chu thuong, so va ky tu dac biet. "
            "Nguoi dung quen mat khau phai dung luong Forgot password va xac minh bang email cong ty. "
            "Khong chia se ma OTP hoac mat khau voi bat ky ai."
        ),
    },
    {
        "id": "doc_mfa_setup",
        "title": "Thiet lap MFA",
        "category": "security",
        "keywords": ["mfa", "2fa", "xac thuc", "otp", "authenticator"],
        "summary_answer": (
            "MFA duoc bat trong Settings > Security > Multi-factor authentication. "
            "He thong uu tien ung dung authenticator; SMS chi dung khi khong the dung app. "
            "Ma khoi phuc phai duoc luu o noi an toan."
        ),
        "text": (
            "Tai lieu bao mat: Bat MFA tai Settings > Security > Multi-factor authentication. "
            "Nguoi dung quet ma QR bang ung dung authenticator, nhap ma OTP de xac nhan, "
            "roi luu recovery codes. SMS la phuong an du phong, khong phai mac dinh."
        ),
    },
    {
        "id": "doc_refund_policy",
        "title": "Chinh sach hoan tien",
        "category": "billing",
        "keywords": ["hoan tien", "refund", "thanh toan", "huy goi", "14 ngay"],
        "summary_answer": (
            "Khach hang co the yeu cau hoan tien trong 14 ngay dau neu chua vuot qua 20% han muc su dung. "
            "Goi nam sau 14 ngay chi duoc quy doi thanh credit noi bo, tru truong hop loi dich vu nghiem trong."
        ),
        "text": (
            "Tai lieu billing: Yeu cau hoan tien duoc chap nhan trong 14 ngay ke tu ngay thanh toan "
            "neu tai khoan chua su dung qua 20% han muc goi. Sau 14 ngay, goi nam khong hoan tien tien mat "
            "ma duoc quy doi thanh credit noi bo, ngoai tru su co dich vu nghiem trong do cong ty xac nhan."
        ),
    },
    {
        "id": "doc_shipping_sla",
        "title": "SLA giao hang thiet bi",
        "category": "operations",
        "keywords": ["giao hang", "thiet bi", "sla", "van chuyen", "doi tra"],
        "summary_answer": (
            "Thiet bi noi dia duoc giao trong 3-5 ngay lam viec. "
            "Neu qua 7 ngay lam viec chua co cap nhat, mo ticket Operations. "
            "Thiet bi loi trong 30 ngay duoc doi moi sau khi xac minh serial."
        ),
        "text": (
            "Tai lieu operations: Don giao thiet bi trong nuoc co SLA 3-5 ngay lam viec. "
            "Don quoc te phu thuoc hai quan va thuong can 7-14 ngay lam viec. "
            "Neu don noi dia qua 7 ngay lam viec khong co cap nhat, nguoi dung can mo ticket Operations. "
            "Thiet bi loi trong 30 ngay duoc doi moi neu serial hop le."
        ),
    },
    {
        "id": "doc_vpn_access",
        "title": "Truy cap VPN",
        "category": "it",
        "keywords": ["vpn", "mang noi bo", "remote", "thiet bi ca nhan", "endpoint"],
        "summary_answer": (
            "VPN chi duoc cap cho nhan su can truy cap he thong noi bo tu xa. "
            "May phai cai endpoint protection, bat MFA va khong duoc dung thiet bi ca nhan chua dang ky."
        ),
        "text": (
            "Tai lieu IT: De truy cap VPN, nhan su nop yeu cau tren IT Portal kem ly do nghiep vu. "
            "Thiet bi phai co endpoint protection, ma hoa dia va MFA. "
            "Thiet bi ca nhan chua dang ky khong duoc phep ket noi VPN."
        ),
    },
    {
        "id": "doc_leave_policy",
        "title": "Chinh sach nghi phep",
        "category": "hr",
        "keywords": ["nghi phep", "phep nam", "hr", "nghi benh", "don nghi"],
        "summary_answer": (
            "Nhan vien toan thoi gian co 12 ngay phep nam. "
            "Don nghi tu 3 ngay lien tiep can gui truoc it nhat 5 ngay lam viec, tru truong hop khan cap."
        ),
        "text": (
            "Tai lieu HR: Nhan vien toan thoi gian co 12 ngay phep nam moi nam. "
            "Yeu cau nghi phep duoc tao tren HR Portal. Don nghi tu 3 ngay lien tiep can gui truoc 5 ngay lam viec. "
            "Nghi benh can giay xac nhan y te neu vuot qua 2 ngay lien tiep."
        ),
    },
    {
        "id": "doc_expense_policy",
        "title": "Hoan ung chi phi",
        "category": "finance",
        "keywords": ["chi phi", "hoa don", "hoan ung", "cong tac", "expense"],
        "summary_answer": (
            "Chi phi cong tac phai nop trong 10 ngay lam viec kem hoa don hop le. "
            "Bua an khong vuot qua 25 USD moi nguoi moi bua neu khong co phe duyet truoc."
        ),
        "text": (
            "Tai lieu finance: Nhan vien nop expense claim trong 10 ngay lam viec sau chuyen cong tac. "
            "Moi khoan chi can hoa don hop le. Dinh muc bua an la 25 USD moi nguoi moi bua. "
            "Chi phi vuot dinh muc can phe duyet cua quan ly truoc khi phat sinh."
        ),
    },
    {
        "id": "doc_data_retention",
        "title": "Luu tru va xoa du lieu",
        "category": "compliance",
        "keywords": ["du lieu", "luu tru", "xoa", "retention", "gdpr", "bao mat"],
        "summary_answer": (
            "Log he thong duoc luu 180 ngay. Du lieu khach hang bi xoa trong 30 ngay sau yeu cau hop le, "
            "tru khi phap ly yeu cau giu lai."
        ),
        "text": (
            "Tai lieu compliance: Log he thong duoc luu 180 ngay de dieu tra su co. "
            "Yeu cau xoa du lieu khach hang duoc xu ly trong 30 ngay sau khi xac minh danh tinh va tinh hop le. "
            "Du lieu co lien quan den tranh chap phap ly co the duoc giu lai theo legal hold."
        ),
    },
    {
        "id": "doc_incident_reporting",
        "title": "Bao cao su co bao mat",
        "category": "security",
        "keywords": ["su co", "bao mat", "incident", "phishing", "mat du lieu"],
        "summary_answer": (
            "Su co bao mat phai duoc bao cao trong 1 gio qua Security Hotline hoac incident form. "
            "Khong tu xoa bang chung; can co lap thiet bi neu nghi nhiem ma doc."
        ),
        "text": (
            "Tai lieu incident: Moi nghi ngo mat du lieu, phishing thanh cong, malware hoac truy cap trai phep "
            "phai duoc bao cao trong 1 gio. Dung Security Hotline hoac incident form. "
            "Nguoi dung khong duoc tu xoa file, log hay email lien quan vi do la bang chung dieu tra."
        ),
    },
    {
        "id": "doc_account_lock",
        "title": "Tai khoan bi khoa",
        "category": "account",
        "keywords": ["khoa tai khoan", "bi khoa", "dang nhap", "login", "that bai", "unlock"],
        "summary_answer": (
            "Tai khoan bi khoa sau 5 lan dang nhap sai lien tiep. "
            "Nguoi dung co the doi 15 phut de mo khoa tu dong hoac lien he IT Service Desk de xac minh danh tinh."
        ),
        "text": (
            "Tai lieu tai khoan: Sau 5 lan dang nhap sai lien tiep, tai khoan bi khoa tam thoi. "
            "He thong tu mo khoa sau 15 phut neu khong co them lan thu sai. "
            "Neu can gap, lien he IT Service Desk va xac minh danh tinh bang email cong ty."
        ),
    },
    {
        "id": "doc_invoice_tax",
        "title": "Hoa don va thue",
        "category": "billing",
        "keywords": ["hoa don", "vat", "thue", "invoice", "ma so thue"],
        "summary_answer": (
            "Hoa don VAT can cap nhat ten cong ty, dia chi va ma so thue truoc ngay phat hanh hoa don. "
            "Sau khi hoa don da phat hanh, yeu cau dieu chinh can gui trong 7 ngay."
        ),
        "text": (
            "Tai lieu billing: De nhan hoa don VAT, khach hang cap nhat day du ten cong ty, dia chi xuat hoa don "
            "va ma so thue truoc ngay phat hanh. Sau khi hoa don da phat hanh, yeu cau dieu chinh thong tin "
            "phai gui trong 7 ngay lam viec."
        ),
    },
    {
        "id": "doc_api_rate_limit",
        "title": "Gioi han API",
        "category": "developer",
        "keywords": ["api", "rate limit", "429", "quota", "retry", "backoff"],
        "summary_answer": (
            "API gioi han 600 request moi phut cho moi workspace. "
            "Khi gap loi 429, client can retry voi exponential backoff va khong retry dong loat."
        ),
        "text": (
            "Tai lieu developer: Moi workspace co gioi han 600 request moi phut. "
            "Neu vuot gioi han, API tra ve HTTP 429 kem header Retry-After. "
            "Ung dung phai retry bang exponential backoff va jitter de tranh retry dong loat."
        ),
    },
]
