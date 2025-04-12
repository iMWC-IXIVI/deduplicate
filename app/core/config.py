import os

from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


class Settings:
    """
    Класс по переменным окружениям в проекте\n
    HOST - Хост clickhouse (имя сервиса в docker"e)\n
    PORT - Порт clickhouse\n
    PASSWORD - Пароль пользователя clickhouse\n
    USERNAME - Логин пользователя clickhouse\n
    DATABASE - Название базы данных в clickhouse\n
    RABBITMQ_URL - Ссылка для подключения к rabbitmq\n
    REDIS_URL - Ссылка для подключения к redis\n
    REDIS_HOST - Хост redis (имя сервиса в docker"e)\n
    REDIS_PORT - Порт redis\n
    """
    # DATABASE ENVIRONMENT
    HOST = os.getenv('CLICKHOUSE_HOST')
    PORT = os.getenv('CLICKHOUSE_PORT')
    PASSWORD = os.getenv('CLICKHOUSE_PASSWORD')
    USERNAME = os.getenv('CLICKHOUSE_USER')
    DATABASE = os.getenv('CLICKHOUSE_DB')
    # URL CONNECTION
    RABBITMQ_URL = os.getenv('RABBITMQ_URL')
    REDIS_URL = os.getenv('REDIS_URL')
    # REDIS ENVIRONMENT
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    # APP ENVIRONMENT
    BASE_DIR = Path(__file__).resolve().parent.parent


settings = Settings()
