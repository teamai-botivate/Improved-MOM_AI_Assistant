import smtplib
from email.mime.text import MIMEText

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "team.ai@botivate.in"
SMTP_PASSWORD = "pjwzgrgaknbqbjca"
EMAIL_FROM = "team.ai@botivate.in"
EMAIL_TO = "prabhatkumarsictc7070@gmail.com"

msg = MIMEText("This is a test email from MOM AI Assistant SMTP setup.")
msg["Subject"] = "SMTP Test"
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO

try:
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
    server.quit()
    print("Test email sent successfully.")
except Exception as e:
    print(f"Failed to send test email: {e}")
