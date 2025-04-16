from datetime import datetime

from celery_app import app
from db.orm import MiniORM
from core import settings, log


def get_data(connect: MiniORM, dt_now: datetime):
    yield from connect.select(['raw_data'], 'original', [('created', '<', dt_now.strftime("%Y-%m-%d %H:%M:%S"))])


@app.task()
def backup_data():
    try:
        connect = MiniORM()
        connect.connect()
    except Exception as e:
        log.error_message(f'Исключение во время подключения к clickhouse - {e}')
        return 'Exception'

    dt_now = datetime.now()

    try:
        log.info_message('Начинается резервное копирование')
        with open(settings.BASE_DIR/'backups'/f'{dt_now.date()}.log', 'w', encoding='utf-8') as file:
            for data in get_data(connect, dt_now):
                file.write(f'{data}\n')
        log.info_message('Резервное копирование завершено')
    except Exception as e:
        log.error_message(f'Исключение во время записи в backup-файл - {e}')
        return 'Exception'

    try:
        log.info_message('Начинается удаление данных из clickhouse')
        connect.connection.execute(f'ALTER TABLE original DELETE WHERE created < \'{dt_now.strftime("%Y-%m-%d %H:%M:%S")}\'')
        connect.connection.execute(f'OPTIMIZE TABLE original FINAL')
        log.info_message('Завершение удаления данных из clickhouse')
    except Exception as e:
        log.error_message(f'Исключение во время удаление данных из clickhouse - {e}')
        return 'Exception'

    return 'Данные успешно скопировались'
