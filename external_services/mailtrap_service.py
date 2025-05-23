from email.mime.text import MIMEText
import smtplib

class EmailService:
    def __init__(self, smtp_server: str, smtp_port: int, mailtrap_user: str, mailtrap_pass: str, from_email: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.mailtrap_user = mailtrap_user
        self.mailtrap_pass = mailtrap_pass
        self.from_email = from_email

    def send_email(self, to_email: str, subject: str, body: str):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.from_email
        msg["To"] = to_email

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.mailtrap_user, self.mailtrap_pass)
            server.send_message(msg)