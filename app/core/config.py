import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    HOST = os.getenv('CLICKHOUSE_HOST')
    PORT = os.getenv('CLICKHOUSE_PORT')
    PASSWORD = os.getenv('CLICKHOUSE_PASSWORD')
    USERNAME = os.getenv('CLICKHOUSE_USER')
    DATABASE = os.getenv('CLICKHOUSE_DB')


settings = Settings()
