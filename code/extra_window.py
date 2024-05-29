from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QMessageBox
from PyQt5.QtCore import Qt

from code.database_dao import DatabaseDAO


class AddWindow(QDialog):
    """Окно для добавления записей в базу данных."""

    def __init__(self, table_names: list, db_dao: DatabaseDAO):
        """
        Конструктор класса.

        Параметры:
        - table_names (list): Список имен таблиц.
        - db_dao (DatabaseDAO): Объект для работы с базой данных.
        """
        super().__init__()

        self.db_dao = db_dao

        self.setWindowTitle("Добавить запись")
        self.setFixedSize(400, 400)  # Фиксированный размер окна

        self.table_names = table_names
        self.fields = {}

        self.layout = QVBoxLayout()

        label_table = QLabel("Выберите таблицу:")
        self.layout.addWidget(label_table)

        self.table_selector = QComboBox()
        self.table_selector.addItems(table_names)
        self.table_selector.currentIndexChanged.connect(self.update_fields)
        self.layout.addWidget(self.table_selector)

        self.fields_layout = QVBoxLayout()
        self.layout.addLayout(self.fields_layout)

        self.update_fields()

        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.add_record)
        self.layout.addWidget(add_button)

        self.setLayout(self.layout)

        self.setStyleSheet("""
            QDialog {
                background-color: lightblue;
            }
            QLabel {
                color: black;
                font-size: 12pt;
            }
            QComboBox, QLineEdit {
                background-color: white;
                color: black;
                font-size: 10pt;
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px;
                height: 20px;
            }
            QPushButton {
                background-color: white;
                color: black;
                font-size: 12pt;
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 black, stop: 1 #333333
                );
                color: white;
            }
        """)

    def update_fields(self):
        """Обновляет поля ввода в зависимости от выбранной таблицы."""
        selected_table = self.table_selector.currentText()

        # Очищаем предыдущие поля
        for i in reversed(range(self.fields_layout.count())):
            self.fields_layout.itemAt(i).widget().setParent(None)

        self.fields = {}

        if selected_table == "classification":
            columns = ["short_name", "name", "id_unit", "id_main_class"]
        elif selected_table == "product":
            columns = ["short_name", "name", "id_class"]
        elif selected_table == "unit":
            columns = ["short_name", "name", "code"]
        else:
            columns = []

        for column in columns:
            label = QLabel(column)
            line_edit = QLineEdit()
            line_edit.setFixedHeight(30)
            self.fields[column] = line_edit
            self.fields_layout.addWidget(label)
            self.fields_layout.addWidget(line_edit)

    def add_record(self):
        selected_table = self.table_selector.currentText()
        data = {column: self.fields[column].text().strip() for column in self.fields}

        try:
            self.insert_data_into_table(selected_table, data)
            QMessageBox.information(self, "Успех", f"Запись успешно добавлена в таблицу {selected_table}.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить запись: {str(e)}")

    def insert_data_into_table(self, table_name, data):
        """Вставляет данные в указанную таблицу."""
        if table_name == "classification":
            query = f"""
            SELECT create_class (%s, %s, %s, %s);
            """
            values = (data["short_name"], data["name"], data["id_unit"], data["id_main_class"])
        elif table_name == "product":
            query = """
            SELECT create_product (%s, %s, %s);
            """
            values = (data["short_name"], data["name"], data["id_class"])
        elif table_name == "unit":
            query = """
            SELECT create_unit (%s, %s, %s);
            """
            values = (data["short_name"], data["name"], data["code"])
        else:
            raise ValueError(f"Неизвестная таблица: {table_name}")

        self.db_dao.cur.execute(query, values)
        self.db_dao.connection.commit()
