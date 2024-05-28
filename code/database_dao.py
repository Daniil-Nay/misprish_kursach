import configparser

import psycopg2
import json

class DatabaseDAO:
    """Data Access Object для работы с базой данных PostgreSQL."""

    def __init__(self, config_file: str, queries_file: str):
        """
        Конструктор класса.

        Параметры:
        - config_file (str): Путь к файлу конфигурации базы данных.
        - queries_file (str): Путь к файлу с SQL-запросами.
        """
        self.config = self._load_config(config_file)
        self.queries = self._load_queries(queries_file)
        self.connection = self._connect()
        self.cur = self.connection.cursor()

    def _load_config(self, config_file: str) -> dict:
        """Загружает конфигурацию базы данных из файла."""
        config = configparser.ConfigParser()
        config.read(config_file)
        return config['postgresql']

    def _load_queries(self, queries_file: str) -> dict:
        """Загружает SQL-запросы из файла."""
        with open(queries_file, 'r') as file:
            return json.load(file)

    def _connect(self):
        """Устанавливает соединение с базой данных."""
        return psycopg2.connect(
            dbname=self.config['dbname'],
            user=self.config['user'],
            password=self.config['password'],
            host=self.config['host'],
            port=self.config['port']
        )

    def execute_query(self, query_key: str, params=None) -> list:
        """
        Выполняет SQL-запрос и возвращает результат.

        Параметры:
        - query_key (str): Ключ запроса в файле queries.json.
        - params (tuple): Параметры запроса (если есть).

        Возвращает:
        - list: Результат выполнения запроса.
        """
        query = self.queries[query_key].format(**(params or {}))
        self.cur.execute(query)
        return self.cur.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.cur.close()
        self.connection.close()
