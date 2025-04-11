from celery import Celery

from core import settings


app = Celery(
    'deduplicate_celery',
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL
)
app.autodiscover_tasks(['celery_app.tasks'])
