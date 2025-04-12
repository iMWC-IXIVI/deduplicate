import uuid
import datetime

from pathlib import Path
from typing import Optional

from core import settings, log
from db.orm import MiniORM


migration_file = Path(__file__).resolve().parent.parent/'migrations'


def get_connection() -> Optional[MiniORM]:
    """Подключение к базе данных"""
    try:
        log.info_message('Начало подключения к БД')
        connect = MiniORM(port=settings.PORT, host=settings.HOST, username=settings.USERNAME, password=settings.PASSWORD, database=settings.DATABASE)
        connect.connect()
        log.info_message('Успешное подключение к БД')
        return connect
    except Exception as e:
        log.error_message(f'Исключение подключения к бд - {e}')


def init_migration() -> None:
    """Инициализация первой таблицы (migration)"""
    try:
        log.info_message('Начало проведения 0001_init_migration.sql')
        with open(migration_file/'0001_init_migration.sql', 'r', encoding='utf-8') as file:
            get_connection().connection.execute(file.read())
        log.info_message('Миграция успешно применена')
    except Exception as e:
        log.error_message(f'Исключение во время инициализации миграций - {e}')


def run_migration() -> None:
    """Применение всех миграций кроме init_migration"""
    connect = get_connection()
    dir_files = sorted([file.name for file in migration_file.glob('*.sql') if file.name != '0001_init_migration.sql'])

    for file_name in dir_files:

        try:
            log.info_message('Операция SELECT в таблицу migration началась')
            data = connect.select(['name_migration'], 'migrations', {'name_migration': f'{file_name}'})
            log.info_message(f'Операция SELECT завершилась успешно, данные: {data}')
        except Exception as e:
            log.error_message(f'MiniORM select не был выполнен - {e}')
            break

        if not data:
            try:
                log.info_message('Начало проведения миграций')
                with open(migration_file/file_name, 'r', encoding='utf-8') as file:
                    connect.connection.execute(file.read())
                log.info_message('Миграции успешно проведены')
            except Exception as e:
                log.error_message(f'MiniORM execute не выполнена миграция - {e}')
                break

            uuid_data = uuid.uuid4()
            dt_data = datetime.datetime.now()

            try:
                log.info_message('Операция INSERT в таблицу migration началась')
                connect.insert('migrations', ['id', 'name_migration', 'time_migration'], [(uuid_data, file_name, dt_data)])
                log.info_message('Операция INSERT завершилась успешно')
            except Exception as e:
                log.error_message(f'MiniORM insert не выполнил вставку данных - {e}')
                break


if __name__ == '__main__':
    # TODO Не сделан откат миграций, в будущих реализаций - ДОБАВИТЬ!!!
    # TODO Рассмотреть тему с ATOMIC REQUESTS в случае возбуждения исключений!!!
    init_migration()
    run_migration()
    log.info_message('Успешное завершение всех миграций')
