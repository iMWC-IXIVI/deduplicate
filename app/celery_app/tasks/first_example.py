from celery_app import app


@app.task
def example(x, y):
    return x * y
