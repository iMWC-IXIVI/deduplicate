import uuid
import json
import hashlib
import redis

from datetime import datetime
from typing import Optional

from core import settings
from db.orm import get_connection


class Deduplicate:
    """
    Класс для дедубликации данных\n
    Deduplicate:\n
    class_attributes:
        REDIS_TTL - Время жизни данных внутри redis\n
        REDIS_CONNECT - Подключение к redis\n
        DB_CONNECT - Подключение к бд (Clickhouse)\n
        TABLE_NAME - Название таблицы в бд (Clickhouse)\n
        S_COLUMNS_NAME - Название колонок для метода select (Clickhouse)\n
        I_COLUMNS_NAME - Название колонок для методы insert (Clickhouse)\n
    __attributes:
        __byte_string: bytes - Строка из данных (Из data)\n
        __hash_data: str - Хэш из полученных данных (Из data)\n
    attributes:
        data: dict - JSON данные о действии пользователя\n
    methods:
        run() -> Optional[bool] - Отбор дублирующих данных\n
    __methods:
        __get_hash() -> None - Получение хэша данных\n
        __check_redis() -> str - Проверка данных внутри redis\n
        __check_db() -> str - Проверка данных внутри бд (Clickhouse)\n
        __save_to_redis() -> None - Сохранение данных в redis (сохранение хэша)\n
        __save_to_db() -> None - Сохранение данных в бд (Clickhouse)\n
    """
    REDIS_TTL = 60
    REDIS_CONNECT = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    DB_CONNECT = get_connection()
    TABLE_NAME = 'original'
    S_COLUMNS_NAME = ['hash', ]
    I_COLUMNS_NAME = ['id', 'hash', 'raw_data', 'created']

    def __init__(self, data: dict) -> None:
        self.data: dict = data

    def run(self) -> Optional[bool]:
        try:
            self.__get_hash()
        except Exception as e:
            print(f'Исключение формирование хэш данных - {e}')
            return

        try:
            if self.__check_redis() == 'Duplicate':
                return False
        except Exception as e:
            print(f'Исключение во время проверки внутри redis - {e}')
            return

        try:
            if self.__check_db() == 'Duplicate':
                return False
        except Exception as e:
            print(f'Исключение во время проверки внутри бд clickhouse - {e}')
            return

        try:
            self.__save_to_redis()
        except Exception as e:
            print(f'Исключение во время сохранение хэша в redis - {e}')
            return

        try:
            self.__save_to_db()
        except Exception as e:
            print(f'Исключение во время сохранения данных в бд clickhouse - {e}')
            return

        return True

    def __get_hash(self) -> None:
        self.__byte_string: bytes = json.dumps(self.data).encode()
        self.__hash_data: str = hashlib.blake2s(self.__byte_string).hexdigest()

    def __check_redis(self) -> str:
        if self.REDIS_CONNECT.exists(self.__hash_data):
            return 'Duplicate'

    def __check_db(self) -> str:
        sql_data = self.DB_CONNECT.select(
            self.S_COLUMNS_NAME,
            self.TABLE_NAME,
            {self.S_COLUMNS_NAME[0]: self.__hash_data}
        )
        if sql_data:
            return 'Duplicate'

    def __save_to_redis(self) -> None:
        self.REDIS_CONNECT.set(self.__hash_data, 'hash')
        self.REDIS_CONNECT.expire(self.__hash_data, self.REDIS_TTL)

    def __save_to_db(self) -> None:
        uuid_data = uuid.uuid4()
        dt_data = datetime.now()

        self.DB_CONNECT.insert(
            self.TABLE_NAME,
            self.I_COLUMNS_NAME,
            [(uuid_data, self.__hash_data, self.__byte_string, dt_data)]
        )
