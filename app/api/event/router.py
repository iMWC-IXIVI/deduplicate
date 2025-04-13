from fastapi import APIRouter

from celery_app import app


router = APIRouter(prefix='/service-event')


@router.post('/')
async def event(data: dict):
    """Обработка событий"""
    app.send_task('celery_app.tasks.deduplicate.deduplicate', args=[data, ])
    return {'message': 'ok'}
