from celery import Celery
from celery.schedules import crontab

from core import settings


app = Celery(
    'deduplicate_celery',
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL
)

app.conf.update(
    include=[
        'celery_app.beat.backup_data',
        'celery_app.worker.deduplicate'
    ]
)
app.conf.timezone = 'Europe/Moscow'
app.conf.enable_utc = False

app.conf.beat_schedule = {
    'backup_data': {
        'task': 'celery_app.beat.backup_data.backup_data',
        'schedule': crontab(hour=0, minute=0, day_of_week=1)
    },
}
