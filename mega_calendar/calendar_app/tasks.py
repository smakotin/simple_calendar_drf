from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_notification(email):
    subject = 'this is a notification'
    message = 'text'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
