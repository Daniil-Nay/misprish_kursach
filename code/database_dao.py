import configparser
import logging

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

    def get_all_from_table(self, table_name):
        query = f"SELECT * FROM {table_name}"
        self.cur.execute(query)
        return self.cur.fetchall()

    def change_product_class(self, change_id_product: int, new_id_class: int):
        """Изменяет класс продукта."""
        query = """
        DO $$
        BEGIN
            IF (SELECT count(*) FROM find_children(%s)) > 1 THEN
                RAISE EXCEPTION 'Продукт может относится только к терминальному классу';
            end if;
            UPDATE Product SET id_class = %s WHERE id_product = %s;
        END;
        $$ LANGUAGE plpgsql;
        """
        values = (new_id_class, new_id_class, change_id_product)
        self.cur.execute(query, values)
        self.connection.commit()

    def find_products_by_class(self, class_id: int) -> list:
        """Находит продукты, принадлежащие указанному классу классификатора."""
        query = """
        SELECT id_product, name
        FROM Product
        WHERE id_class = %s
        """
        self.cur.execute(query, (class_id,))
        return self.cur.fetchall()

    def find_children_by_class(self, class_id: int) -> list:
        query = """
        SELECT id_class, short_name
        FROM find_children(%s)
        """
        try:
            self.cur.execute(query, (class_id,))
            return self.cur.fetchall()
        except psycopg2.Error as e:
            logging.error(f"Ошибка выполнения запроса: {e.pgerror}")
            raise
    def change_parent_class(self, child_id_class: int, new_parent_id_class: int):
        """Изменяет родителя указанного класса."""
        query = """
        DO $$
        DECLARE
            hasCycle boolean;
        BEGIN
            hasCycle = cycle(%s, %s);
            if hasCycle then
                RAISE EXCEPTION 'Нельзя поменять родителя, потому что создается цикл';
            else
                UPDATE classification SET id_main_class = %s WHERE id_class = %s;
            end if;
        END;
        $$ LANGUAGE plpgsql;
        """
        values = (child_id_class, new_parent_id_class, new_parent_id_class, child_id_class)
        self.cur.execute(query, values)
        self.connection.commit()
