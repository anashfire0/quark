from celery import shared_task
from django.core.mail import send_mail
from .models import Reminder

@shared_task
def raka(s):
    return s

@shared_task
def emailer():
    send_mail('test subject', 'test body', 'Reminder@quark.com',
     ['ashsixthree.63@gmail.com'])
    return 'YAY!!!!!!!!!'.center(1000, '$')

@shared_task
def email_reminder(subject, body, sender, receiver, slug):
    try:
        Reminder.objects.get(slug__iexact=slug)
    except Reminder.DoesNotExist:
        return 'The reminder was edited/deleted.'
    send_mail(subject, body, sender, [receiver])
    return f'{receiver} recieved the email.'