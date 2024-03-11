
from celery import shared_task
import time

@shared_task
def hello():
    time.sleep(2)
    print("Hello, world!")