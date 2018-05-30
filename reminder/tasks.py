from celery import shared_task

@shared_task
def raka(s):
    return s.center(1500, '#')