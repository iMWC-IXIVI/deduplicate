from typing import List, Tuple, Any, Dict, Optional

from clickhouse_driver import Client


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
        select(columns, table, condition=None) -> Optional[List[Tuple[Any, ...]]]: Метод по получении данных
            attributes:
                columns: List[str] - Названия колонок в бд (clickhouse)\n
                table: str - Название таблицы в бд (clickhouse)\n
                condition: Optional[Dict[str, str]] = None - Условия поиска\n
        connect() -> Client - Метод по подключению к бд (clickhouse)\n
        test_connection() -> bool - Подключение-тест к ьд (clickhouse)\n
    """
    def __init__(self, **kwargs) -> None:
        self.host: str = kwargs.get('host', 'localhost')
        self.port: int = kwargs.get('port', 9000)
        self.database: str = kwargs.get('database', 'default')
        self.username: str = kwargs.get('username', 'default')
        self.password: str = kwargs.get('password', '')

        self.connection: Optional[Client] = None

    def insert(self, table: str, columns: List[str], values: List[Tuple[Any, ...]]):
        if not self.test_connection():
            return

        safe_columns = [f'`{column}`' for column in columns]
        safe_table = f'`{table}`'

        sql = f'INSERT INTO {safe_table} ({f", ".join(safe_columns)}) VALUES'

        self.connection.execute(query=sql, params=values)

    def select(self, columns: List[str], table: str, condition: Optional[Dict[str, str]] = None):
        if not self.test_connection():
            return

        safe_columns = [f'`{column}`' for column in columns]

        safe_table = f'`{table}`'

        query_sql = f'SELECT {", ".join(safe_columns)} FROM {safe_table}'

        if condition:
            safe_condition = [f'`{key}` = %({key})s' for key in condition]
            query_sql += f' WHERE {" AND ".join(safe_condition)}'

        data = self.connection.execute(query=query_sql, params=condition)
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
            print(f'Исключение {e}')
            return False
