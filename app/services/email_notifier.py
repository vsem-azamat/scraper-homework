import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailNotifierInterface:
    def __init__(
        self,
        smtp_server: str,
        port: int,
        sender_email: str,
        password: str,
        receiver_email: str,
    ) -> None:
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.password = password
        self.receiver_email = receiver_email

    def send_email(self, subject: str, body: str) -> None:
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, message.as_string())
