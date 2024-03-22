from celery import shared_task

from common.mail import Mail
from common.services import make_url
from parking_project import settings


@shared_task
def send_activation_link(user):
    Mail(
        to=[user["email"]],
        subject="Account Activation",
        from_email=settings.SUPPORT_EMAIL,
    ).template(
        "activation.html",
        {
            "link": make_url("login"),
            "first_name": user["first_name"],
            "last_name": user["last_name"],
        },
    ).queue()
