import datetime
from celery import shared_task


@shared_task(name="health_test")
def test():
    print("hi celery task in time 10 s")