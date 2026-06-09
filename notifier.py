import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

EMAIL_FROM = "bensammanuel@gmail.com"
EMAIL_TO   = "bensammanuel@gmail.com"
EMAIL_PASS = "rphwkqakpdtskjkw"


def send_email(subject, body, html=None, pdf_path=None):
    try:
        msg = MIMEMultipart("mixed")
        msg["From"]    = EMAIL_FROM
        msg["To"]      = EMAIL_TO
        msg["Subject"] = subject

        # Body
        alt = MIMEMultipart("alternative")
        alt.attach(MIMEText(body, "plain"))
        if html:
            alt.attach(MIMEText(html, "html"))
        msg.attach(alt)

        # PDF attachment
        if pdf_path:
            with open(pdf_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            import os
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(pdf_path)}")
            msg.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASS)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

        print("Email sent.", flush=True)
    except Exception as e:
        print(f"Email failed: {e}", flush=True)
