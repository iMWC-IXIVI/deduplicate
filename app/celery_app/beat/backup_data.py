from celery_app import app

from datetime import datetime


@app.task()
def say_hello():
    print(datetime.now())
