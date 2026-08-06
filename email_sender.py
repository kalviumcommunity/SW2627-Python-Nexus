import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_report(report_text: str, recipient: str) -> tuple[bool, str]:
    """
    Sends the generated report via SMTP using environment credentials.
    Implements non-blocking error handling so failures return status without crashing.
    """
    sender = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("SENDER_PASSWORD")
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))

    if not sender or not password:
        msg = "Email credentials missing in environment variables (SENDER_EMAIL / SENDER_PASSWORD)."
        print(f"Warning: {msg}")
        return False, msg

    if not recipient:
        return False, "Recipient email address is required."

    msg = MIMEMultipart()
    msg["Subject"] = "Weekly Analytics Report Summary"
    msg["From"] = sender
    msg["To"] = recipient

    msg.attach(MIMEText(report_text, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        return True, f"Report successfully emailed to {recipient}!"
    except Exception as e:
        # Non-blocking error handling: catch error, log it, and return false
        error_msg = f"Failed to send email: {str(e)}"
        print(error_msg)
        return False, error_msg