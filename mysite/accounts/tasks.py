from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mail_view(receiver_email, message):
    send_mail(
        "Account-related messages by polls site",
        message,
        "django@email.test",
        [receiver_email],
        fail_silently=False,
    )
