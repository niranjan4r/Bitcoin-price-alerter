import smtplib
from email.mime.text import MIMEText

def send_email(email_cfg, subject, body):
    recipients = email_cfg["recipient_emails"]

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = email_cfg["sender"]
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP(email_cfg["smtp_server"], email_cfg["smtp_port"]) as server:
        server.starttls()
        server.login(email_cfg["sender"], email_cfg["password"])
        server.send_message(msg)

    print(f"Alert sent to {', '.join(recipients)}")
