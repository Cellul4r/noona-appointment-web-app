from re import DEBUG

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from app.config import settings
from app.schemas.email import EmailSchema


class EmailService:

    def __init__(self):
        self.fm = FastMail(self.get_connection_config())

    def get_connection_config(self):
        return ConnectionConfig(
            MAIL_USERNAME=settings.mail_username,
            MAIL_PASSWORD=settings.mail_password,
            MAIL_FROM=settings.mail_from,
            MAIL_FROM_NAME=settings.mail_from_name,
            MAIL_PORT=settings.mail_port,
            MAIL_SERVER=settings.mail_server,
            MAIL_SSL_TLS=settings.mail_ssl_tls,
            MAIL_STARTTLS=settings.mail_starttls,
            USE_CREDENTIALS=settings.use_credentials,
            VALIDATE_CERTS=settings.validate_certs,
        )

    async def send_emails(self, subject: str, email: EmailSchema, html: str):
        message = MessageSchema(
            subject=subject,
            recipients=email.model_dump().get("email"),
            body=html,
            subtype=MessageType.html,
        )

        await self.fm.send_message(message)
        return {"message": "Email has been sent"}
