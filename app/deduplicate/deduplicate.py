import uuid
import json
import hashlib
import redis

from datetime import datetime
from typing import Optional

from core import settings, log
from db.orm import get_connection
from bloom_filter import BloomFilter


class Deduplicate:
    """
    Класс для дедубликации данных\n
    Deduplicate:\n
    class_attributes:
        BLOOM - Фильтр Блума\n
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
    BLOOM = BloomFilter(10_000_000, 0.01)
    REDIS_TTL = 60
    REDIS_CONNECT = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    DB_CONNECT = get_connection()
    TABLE_NAME = 'original'
    S_COLUMNS_NAME = ['hash', ]
    I_COLUMNS_NAME = ['id', 'hash', 'raw_data', 'created']

    def __init__(self, data: dict) -> None:
        self.data: dict = data

    def run(self) -> Optional[bool]:
        log.info_message('Начинается проверка на дубликат')

        try:
            log.info_message('Начинается проверка внутри bloom')
            if self.BLOOM.is_contains(self.data):
                return False
            log.info_message('Проверка в bloom\'е завершилась успешно')
        except Exception as e:
            log.error_message(f'Исключение во время работы BloomFilter - {e}')
            return

        try:
            log.info_message('Создание хэша данных')
            self.__get_hash()
            log.info_message('Хэш успешно создан')
        except Exception as e:
            log.error_message(f'Исключение формирование хэш данных - {e}')
            return

        try:
            log.info_message('Манипуляция с redis началась')
            if self.__manipulation_redis() == 'Duplicate':
                log.warning_message(f'Дубликат найден, хэш - {self.__hash_data}')
                return False
            log.info_message('Манипуляция успешно завершилась')
        except Exception as e:
            log.error_message(f'Исключение во время работы с redis - {e}')
            return

        try:
            log.info_message('Проверка хэша в clickhouse (бд)')
            if self.__check_db() == 'Duplicate':
                log.warning_message(f'Дублика найден, хэш - {self.__hash_data}')
                return False
            log.info_message('Проверка успешно пройдена')
        except Exception as e:
            log.error_message(f'Исключение во время проверки внутри бд clickhouse - {e}')
            return

        try:
            log.info_message('Начинается сохранение данных в bloom filter')
            self.BLOOM.add_item(self.data)
            log.info_message('Сохранение данных в bloom filter прошла успешно')
        except Exception as e:
            log.error_message(f'Исключение во время сохранения данных в bloom filter - {e}')
            return

        try:
            log.info_message('Начинается сохранение данных в clickhouse (бд)')
            self.__save_to_db()
            log.info_message('Данные успешно сохранены в clickhouse (бд)')
        except Exception as e:
            log.error_message(f'Исключение во время сохранения данных в бд clickhouse - {e}')
            return

        log.info_message('Данные успешно проверены на дубликат. Дубликат не найден')

        return True

    def __get_hash(self) -> None:
        self.__byte_string: bytes = json.dumps(self.data, sort_keys=True).encode()
        self.__hash_data: str = hashlib.blake2s(self.__byte_string).hexdigest()

    def __manipulation_redis(self) -> str:
        if not self.REDIS_CONNECT.set(self.__hash_data, 'hash', nx=True, ex=60):
            return 'Duplicate'

    def __check_db(self) -> str:
        sql_data = self.DB_CONNECT.select(
            self.S_COLUMNS_NAME,
            self.TABLE_NAME,
            [(self.S_COLUMNS_NAME[0], '=', self.__hash_data)]
        )
        if sql_data:
            return 'Duplicate'

    def __save_to_db(self) -> None:
        uuid_data = uuid.uuid4()
        dt_data = datetime.now()

        self.DB_CONNECT.insert(
            self.TABLE_NAME,
            self.I_COLUMNS_NAME,
            [(uuid_data, self.__hash_data, self.__byte_string, dt_data)]
        )
