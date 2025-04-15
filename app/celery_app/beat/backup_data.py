from datetime import datetime

from celery_app import app
from db.orm import MiniORM
from core import settings


connect = MiniORM()
connect.connect()
dt_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_data():
    yield from connect.connection.execute(f'SELECT raw_data FROM original WHERE created < \'{dt_now}\'')


@app.task()
def say_hello():
    with open(settings.BASE_DIR/'backups'/f'{datetime.now().date()}.log', 'w', encoding='utf-8') as file:
        for data in get_data():
            file.write(f'{data}\n')
    connect.connection.execute(f'DELETE FROM original WHERE created < \'{dt_now}\'')
    connect.connection.execute(f'OPTIMIZE TABLE original FINAL')
    return 'Данные успешно скопировались'
