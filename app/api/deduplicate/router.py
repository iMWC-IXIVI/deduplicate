from fastapi import APIRouter

from celery_app import app


router = APIRouter(prefix='/deduplicate')


@router.get('/')
async def example(data: dict):
    app.send_task('celery_app.tasks.deduplicate.deduplicate', args=[data, ])
    return {'message': 'ok'}
