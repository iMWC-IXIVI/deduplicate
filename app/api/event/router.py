from fastapi import APIRouter, requests

from celery_app import app


router = APIRouter(prefix='/service-event')


@router.post('/')
async def event(request: requests.Request):
    """Обработка событий"""
    data = await request.json()
    app.send_task('celery_app.worker.deduplicate.deduplicate', args=[data, ])
    return {'message': 'ok'}
