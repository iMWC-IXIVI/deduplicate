from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

from core import settings


app = Celery(
    'deduplicate_celery',
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL
)
# app.autodiscover_tasks(['celery_app.worker', 'celery_app.beat'])
app.conf.update(
    include=[
        'celery_app.beat.backup_data',
        'celery_app.worker.deduplicate'
    ]
)

app.conf.beat_schedule = {
    'say_hello_message': {
        'task': 'celery_app.beat.backup_data.say_hello',
        'schedule': timedelta(days=5)
    },
}
