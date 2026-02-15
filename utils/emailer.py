import smtplib
from dotenv import load_dotenv  # ✅ Load .env
from email.message import EmailMessage
import os


# ✅ Load environment variables from .env file
load_dotenv()

EMAIL_ADDRESS = os.getenv("BILLING_EMAIL", "youremail@example.com")
EMAIL_PASSWORD = os.getenv("BILLING_PASS", "yourpassword")

def send_invoice_pdf(email_to, file_path):
    msg = EmailMessage()
    msg['Subject'] = 'Your Invoice from BillingSoft Pro'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email_to

    msg.set_content("Dear Customer,\n\nPlease find your invoice attached.\n\nThanks,\nBillingSoft Pro")

    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(file_path)
            msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"[✓] Email sent to {email_to} with attachment {file_name}")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")
        raise
