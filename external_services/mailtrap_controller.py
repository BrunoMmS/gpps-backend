from fastapi import APIRouter, BackgroundTasks
from external_services.mailtrap_schema import EmailSchema
from external_services.mailtrap_service import EmailService 
import os

mailtrap_router = APIRouter(prefix="/email", tags=["email"])


class EmailController:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    def send_email_endpoint(self, email: EmailSchema, background_tasks: BackgroundTasks):
        background_tasks.add_task(
            self.email_service.send_email, email.email, email.subject, email.body
        )
        return {"message": "Email enviado correctamente"}

MAILTRAP_USER = os.getenv("MAILTRAP_USER")
MAILTRAP_PASS = os.getenv("MAILTRAP_PASS")

email_service = EmailService(
    smtp_server="sandbox.smtp.mailtrap.io",
    smtp_port=587,
    mailtrap_user=MAILTRAP_USER,
    mailtrap_pass=MAILTRAP_PASS,
    from_email="from@example.com"
)

email_controller = EmailController(email_service)

@mailtrap_router.post("/send/")
def send_email_api(email: EmailSchema, background_tasks: BackgroundTasks):
    return email_controller.send_email_endpoint(email, background_tasks)