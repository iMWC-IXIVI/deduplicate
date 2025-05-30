from typing import List, Tuple, Any, Dict, Optional

from clickhouse_driver import Client

from core import settings, log


class MiniORM:
    """
    Класс-реализация минималистичная orm система для Clickhouse\n
    MiniORM:\n
    attributes:
        host: str - Хост clickhouse (имя сервиса в docker"e): default localhost\n
        port: int - Порт clickhouse: default 9000\n
        database: str - Название базы данных в clickhouse: default default\n
        username: str - Логин пользователя (clickhouse): default default\n
        password: str - Пароль пользователя (clickhouse): default ""\n
        connection: str - Кэш-подключение к базе данных (clickhouse): default None\n
    methods:
        insert(table, columns, values) -> None: Метод по добавлении записи в бд
            attributes:
                table: str - Название таблицы в бд (clickhouse)\n
                columns: List[str] - Название колонок в бд (clickhouse)\n
                values: List[Tuple[Any, ...]] - Значения колонок в бд (clickhouse)\n
        select(columns, table, condition=None, separation=AND) -> Optional[List[Tuple[Any, ...]]]: Метод по получении данных
            attributes:
                columns: List[str] - Названия колонок в бд (clickhouse)\n
                table: str - Название таблицы в бд (clickhouse)\n
                condition: Optional[List[Tuple[str, str, str]]] = None - Условия поиска\n
                separation: str = AND - Соединитель\n
        connect() -> Client - Метод по подключению к бд (clickhouse)\n
        test_connection() -> bool - Подключение-тест к ьд (clickhouse)\n
    """
    def __init__(self, **kwargs) -> None:
        self.host: str = kwargs.get('host', settings.HOST)
        self.port: int = kwargs.get('port', settings.PORT)
        self.database: str = kwargs.get('database', settings.DATABASE)
        self.username: str = kwargs.get('username', settings.USERNAME)
        self.password: str = kwargs.get('password', settings.PASSWORD)

        self.connection: Optional[Client] = None

    def insert(self, table: str, columns: List[str], values: List[Tuple[Any, ...]]):
        if not self.test_connection():
            return

        safe_columns = [f'`{column}`' for column in columns]
        safe_table = f'`{table}`'

        sql = f'INSERT INTO {safe_table} ({f", ".join(safe_columns)}) VALUES'

        self.connection.execute(query=sql, params=values)

    def select(
            self,
            columns: List[str], table: str,
            condition: Optional[List[Tuple[str, str, str]]] = None,
            separation: str = 'AND'
    ):
        if not self.test_connection():
            return

        if separation not in {'AND', 'OR'}:
            raise ValueError('Данная операция не возможна')

        safe_columns = [f'`{column}`' for column in columns]
        safe_table = f'`{table}`'
        separation = f' {separation} '

        query_sql = f'SELECT {", ".join(safe_columns)} FROM {safe_table}'

        params = {}
        query_list = []
        if condition:
            for key, sep_condition, value in condition:
                if sep_condition not in ['=', '!=', '<>', '>', '<', '>=', '<=', '<=>']:
                    raise ValueError('Данный тип операций не поддерживается')
                query_list.append(f'`{key}` {sep_condition} %({key})s')
                params.update({key: value})

        query_sql += f' WHERE {separation.join(query_list)}'

        data = self.connection.execute(query=query_sql, params=params)

        return data

    def connect(self):
        """Подключение к бд Clickhouse"""
        if not self.connection:
            self.connection = Client(host=self.host, port=self.port, database=self.database, user=self.username, password=self.password)
            return self.connection
        return self.connection

    def test_connection(self):
        """Проверка подключения к бд"""
        try:
            self.connect().execute('SELECT 1')
            return True
        except Exception as e:
            log.error_message(f'Исключение {e}')
            return False
