from PyQt5.QtWidgets import QLabel, QScrollArea, QPushButton, QWidget, QVBoxLayout, QLineEdit, QDialog, QMessageBox

from code.constants import file_path
from code.database_dao import DatabaseDAO


class FindProductsWindow(QDialog):
    def __init__(self, db_dao: DatabaseDAO):
        super().__init__()

        self.db_dao = db_dao
        self.setWindowTitle("Найти продукты по классу")
        self.setFixedSize(400, 300)  # Фиксированный размер окна

        self.layout = QVBoxLayout()

        self.class_id_input = QLineEdit(self)
        self.class_id_input.setPlaceholderText("ID класса")
        self.layout.addWidget(self.class_id_input)

        search_button = QPushButton("Поиск", self)
        search_button.clicked.connect(self.find_products)
        self.layout.addWidget(search_button)

        self.results_area = QScrollArea(self)
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        self.results_area.setWidget(self.results_widget)
        self.results_area.setWidgetResizable(True)
        self.layout.addWidget(self.results_area)
        try:
            with open(file_path, 'r') as file:
                styles = file.read()
            self.setStyleSheet(styles)
        except FileNotFoundError:
            print("Файл стилей не найден.")
        except Exception as e:
            print(f"Ошибка при чтении файла стилей: {e}")

        self.setLayout(self.layout)

    def find_products(self):
        """Вызывается при нажатии на кнопку 'Поиск'."""
        try:
            class_id = int(self.class_id_input.text())
            results = self.db_dao.find_products_by_class(class_id)
            self.display_results(results)
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Введите корректное числовое значение.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить поиск: {str(e)}")

    def display_results(self, results):
        """Отображает результаты поиска в окне."""
        for i in reversed(range(self.results_layout.count())):
            self.results_layout.itemAt(i).widget().setParent(None)

        if results:
            for result in results:
                label = QLabel(f"ID продукта: {result[0]}, Название: {result[1]}")
                self.results_layout.addWidget(label)
        else:
            label = QLabel("Продукты не найдены.")
            self.results_layout.addWidget(label)