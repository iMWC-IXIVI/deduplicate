class Deduplicate:
    """
    Класс для дедубликации данных\n
    Deduplicate:\n
    class_attributes:
        REDIS_TTL - Время жизни данных внутри redis\n
        REDIS_CONNECT - Подключение к redis\n
        DB_CONNECT - Подключение к бд (Clickhouse)\n
    attributes:
        data - JSON данные о действии пользователя\n
    methods:
        run() - Отбор дублирующих данных\n
    __methods:
        __get_hash() - Получение хэша данных\n
        __check_redis() - Проверка данных внутри redis\n
        __check_db() - Проверка данных внутри бд (Clickhouse)\n
        __save_to_redis() - Сохранение данных в redis (сохранение хэша)\n
        __save_to_db() - Сохранение данных в бд (Clickhouse)\n
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
