from mini_orm import MiniORM

from pathlib import Path

from core import settings


migration_file = Path(__file__).resolve().parent.parent
connect = MiniORM(host=settings.HOST, username=settings.USERNAME, password=settings.PASSWORD, database=settings.DATABASE).connect()

with open(f'{migration_file}/migrations/0001_init_migration.sql', 'r', encoding='utf-8') as file:
    connect.execute(file.read())
