from typing import List, Tuple, Any, Dict, Optional

from clickhouse_driver import Client


class MiniORM:
    def __init__(self, **kwargs) -> None:
        self.host: str = kwargs.get('host', 'localhost')
        self.port: int = kwargs.get('port', 9000)
        self.database: str = kwargs.get('database', 'default')
        self.username: str = kwargs.get('username', 'default')
        self.password: str = kwargs.get('password', '')

        self.connection: Optional[Client] = None

    def insert(self, table: str, columns: List[str], values: List[Tuple[Any, ...]]):
        """Создание записи в бд"""
        if not self.test_connection():
            return

        safe_columns = [f'`{column}`' for column in columns]
        safe_table = f'`{table}`'

        sql = f'INSERT INTO {safe_table} ({f", ".join(safe_columns)}) VALUES'

        self.connection.execute(query=sql, params=values)

    def select(self, columns: List[str], table: str, condition: Optional[Dict[str, str]] = None):
        """Получение данных из бд"""
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


test = MiniORM(username='admin', password='admin', database='deduplicate')
test.connect()
print(test.test_connection())
print(test.insert('users', ['name', 'age', 'surname'], [('Aboba', 32, 'Abobovih'), ('Bboba', 332, 'BAbobovih')]))
