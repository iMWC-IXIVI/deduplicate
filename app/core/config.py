import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    HOST = os.getenv('CLICKHOUSE_HOST')
    PORT = os.getenv('CLICKHOUSE_PORT')
    PASSWORD = os.getenv('CLICKHOUSE_PASSWORD')
    USERNAME = os.getenv('CLICKHOUSE_USER')
    DATABASE = os.getenv('CLICKHOUSE_DB')

    RABBITMQ_URL = os.getenv('RABBITMQ_URL')
    REDIS_URL = os.getenv('REDIS_URL')

    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')


settings = Settings()
