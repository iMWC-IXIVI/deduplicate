from fastapi import APIRouter

from celery_app import app


router = APIRouter(prefix='/deduplicate')


@router.get('/')
async def example():
    app.send_task('celery_app.tasks.first_example.example', args=[3, 4])
    return {'message': 'ok'}
