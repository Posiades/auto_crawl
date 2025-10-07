import smtplib
from email.message import EmailMessage
from pathlib import Path

def send_mail():
    # === Cấu hình thông tin gửi ===
    EMAIL_SENDER = "c9smoothie1995@gmail.com"
    EMAIL_PASSWORD = "lvop nlzc vbay znwg"
    EMAIL_RECEIVER = "thachnguyenngoc2504@gmail.com"

    # === Xác định thư mục chứa file Excel ===
    base_dir = Path(__file__).resolve().parent.parent  # Thư mục Crawl/
    update_dir = base_dir / "excel" / "link" / "win_link"

    # === Tìm file mới nhất trong thư mục update ===
    excel_files = sorted(update_dir.glob("result_*.xlsx"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not excel_files:
        raise FileNotFoundError("Không tìm thấy file Excel nào trong thư mục update/")
    latest_file = excel_files[0]

    print(f"📁 File mới nhất: {latest_file.name}")

    # === Tạo email ===
    msg = EmailMessage()
    msg["Subject"] = f"Báo cáo tự động: {latest_file.name}"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content("Chào bạn,\nĐính kèm là file Excel mới nhất.\n\nThân mến,\nThạch")

    # === Đính kèm file ===
    with open(latest_file, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=latest_file.name
        )

    # === Gửi email ===
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("Gửi mail thành công!")
