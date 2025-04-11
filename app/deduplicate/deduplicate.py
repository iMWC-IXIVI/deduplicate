class Deduplicate:
    """
    Класс для дедубликации данных
    Deduplicate:
    class_attributes:
        REDIS_TTL - Время жизни данных внутри redis
        REDIS_CONNECT - Подключение к redis
        DB_CONNECT - Подключение к бд (Clickhouse)
    attributes: data - JSON данные о действии пользователя
    methods: run() - Отбор дублирующих данных
    __methods:
        __get_hash() - Получение хэша данных
        __check_redis() - Проверка данных внутри redis
        __check_db() - Проверка данных внутри бд (Clickhouse)
        __save_to_redis() - Сохранение данных в redis (сохранение хэша)
        __save_to_db() - Сохранение данных в бд (Clickhouse)
    """
    REDIS_TTL = ...
    REDIS_CONNECT = ...
    DB_CONNECT = ...

    def __init__(self):
        ...

    def run(self):
        ...

    def __get_hash(self):
        ...

    def __check_redis(self):
        ...

    def __check_db(self):
        ...

    def __save_to_redis(self):
        ...

    def __save_to_db(self):
        ...
