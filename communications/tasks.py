from celery import shared_task
from django.core.mail import send_mail
from time import sleep

@shared_task
def print_to_console(text="testing celery ..."):
    print(text)

@shared_task
def send_email_task(subject,message,fromMail,toArr):
    "about to send mail..."
    send_mail(subject,message,fromMail,toArr)
    return None

# @shared_task
# def error_handler(request, exc, traceback):
#     print('Task {0} raised exception: {1!r}\n{2!r}'.format(
#           request.id, exc, traceback))