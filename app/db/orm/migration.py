import uuid
import datetime

from pathlib import Path

from core import settings
from db.orm import MiniORM


migration_file = Path(__file__).resolve().parent.parent/'migrations'


def get_connection() -> MiniORM:
    """Подключение к базе данных"""
    connect = MiniORM(port=settings.PORT, host=settings.HOST, username=settings.USERNAME, password=settings.PASSWORD, database=settings.DATABASE)
    connect.connect()

    return connect


def init_migration() -> None:
    """Инициализация первой таблицы (migration)"""
    with open(migration_file/'0001_init_migration.sql', 'r', encoding='utf-8') as file:
        get_connection().connection.execute(file.read())


def run_migration() -> None:
    """Применение всех миграций кроме init_migration"""
    connect = get_connection()
    dir_files = sorted([file.name for file in migration_file.glob('*.sql') if file.name != '0001_init_migration.sql'])

    for file_name in dir_files:
        data = connect.select(['name_migration'], 'migrations', {'name_migration': f'{file_name}'})

        if not data:
            with open(migration_file/file_name, 'r', encoding='utf-8') as file:
                connect.connection.execute(file.read())

            uuid_data = uuid.uuid4()
            dt_data = datetime.datetime.now()
            connect.insert('migrations', ['id', 'name_migration', 'time_migration'], [(uuid_data, file_name, dt_data)])


if __name__ == '__main__':
    # TODO Не сделан откат миграций, в будущих реализаций - ДОБАВИТЬ!!!
    # TODO Рассмотреть тему с ATOMIC REQUESTS в случае возбуждения исключений!!!
    init_migration()
    run_migration()
