import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication, QScrollArea, QGridLayout, QMainWindow
from PyQt5.QtCore import Qt

from code.extra_window import AddWindow
from code.view import TableView
from code.static_funcs import get_russian_table_name
from code.database_dao import DatabaseDAO


class Controller:
    """Контроллер для управления главным окном приложения."""

    def __init__(self, root: QMainWindow):
        """
        Конструктор класса.

        Параметры:
        - root (QMainWindow): Главное окно приложения.
        """
        self.root = root
        root.resize(800, 600)

        # Инициализация DatabaseDAO
        self.db_dao = DatabaseDAO('database.ini', 'queries.json')

        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: lightblue;")

        self.layout = QVBoxLayout(self.central_widget)
        self.root.setCentralWidget(self.central_widget)

        self.scroll_area = QScrollArea(self.central_widget)
        self.scroll_area.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical {
                background: #f1f1f1;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border: 2px solid black;
            }
            QScrollBar::handle:vertical {
                background: #888;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                subcontrol-origin: margin;
                subcontrol-position: bottom;
                height: 0px;
                width: 0px;
            }
            QScrollBar::sub-line:vertical {
                subcontrol-origin: margin;
                subcontrol-position: top;
                height: 0px;
                width: 0px;
            }
        """)

        self.layout.addWidget(self.scroll_area)

        self.inner_widget = QWidget()
        self.inner_widget.setStyleSheet("background-color: white;")
        self.inner_layout = QVBoxLayout(self.inner_widget)

        self.scroll_area.setWidget(self.inner_widget)
        self.scroll_area.setWidgetResizable(True)

        self.view = TableView(self.inner_widget)
        self.inner_layout.addWidget(self.view)

        self.button_layout = QGridLayout()
        self.layout.addLayout(self.button_layout)

        self.buttons = []

        self.create_table_buttons()

        self.update_view()

        self.create_add_button()

    def create_table_buttons(self):
        """Создает кнопки для отображения данных каждой таблицы."""
        table_names = self.get_table_names()
        row, col = 0, 0
        for name in table_names:
            russian_name = get_russian_table_name(name[0])
            button = QPushButton(russian_name, self.central_widget)
            button.clicked.connect(lambda _, table=name[0]: self.show_table_data(table))
            self.style_button(button)
            self.buttons.append(button)
            self.button_layout.addWidget(button, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def style_button(self, button: QPushButton):
        """Применяет стилизацию к кнопке."""
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold;
                border: 2px solid black;
                padding: 10px;
                border-radius: 15px;
                font-size: 12pt;
                transition: all 0.2s ease;
                box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 black, stop: 1 #333333
                );
                color: white;
            }
        """)

    def get_table_names(self) -> list:
        """Возвращает список имен всех таблиц в базе данных."""
        return self.db_dao.execute_query("get_table_names")

    def show_table_data(self, table_name: str):
        """Отображает данные из выбранной таблицы."""
        result = self.db_dao.execute_query("select_all_from_table", {"table_name": table_name})
        if result:
            column_names = [description[0] for description in self.db_dao.cur.description]
            print(f"Названия столбцов:", column_names)
            print(f"Данные из таблицы {table_name}:", *result, sep="\n")
            self.view.update_data(result, column_names)
        else:
            print("Таблица пуста")

    def update_view(self):
        """Обновляет вид отображения, показывая данные из первой таблицы."""
        table_names = self.get_table_names()
        if table_names:
            table_name = table_names[0][0]
            self.show_table_data(table_name)

    def create_add_button(self):
        """Создает кнопку для добавления записи в выбранную таблицу."""
        add_button = QPushButton("+", self.central_widget)
        add_button.clicked.connect(self.open_add_window)
        self.style_button(add_button)
        self.button_layout.addWidget(add_button)

    def open_add_window(self):
        """Открывает окно для добавления новой записи."""
        table_names = self.get_table_names()
        add_window = AddWindow(table_names, self.db_dao)
        add_window.exec_()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    root = QMainWindow()
    controller = Controller(root)
    root.show()
    sys.exit(app.exec_())
