from celery_app import app

from deduplicate import Deduplicate


@app.task
def deduplicate(data: dict):
    dedup = Deduplicate(data)
    result = dedup.run()

    if not result:
        return 'Duplicate'
    return 'Success'
