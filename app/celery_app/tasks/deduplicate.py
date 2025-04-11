from celery_app import app

from deduplicate import Deduplicate


@app.task
def deduplicate(data: dict):
    """Задача по выявлению дубликатов"""
    dedup = Deduplicate(data)
    result = dedup.run()

    if not result:
        return 'Duplicate'
    return 'Success'
