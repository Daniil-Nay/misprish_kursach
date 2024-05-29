import os

from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QMessageBox, QPushButton

from code.constants import file_path
from code.database_dao import DatabaseDAO


class ChangeClassWindow(QDialog):
    def __init__(self, db_dao: DatabaseDAO):
        super().__init__()

        self.db_dao = db_dao
        self.setWindowTitle("Изменить класс продукта")
        self.setFixedSize(300, 200)  # Фиксированный размер окна

        self.layout = QVBoxLayout()

        self.product_id_input = QLineEdit(self)
        self.product_id_input.setPlaceholderText("ID продукта")
        self.layout.addWidget(self.product_id_input)

        self.new_class_id_input = QLineEdit(self)
        self.new_class_id_input.setPlaceholderText("Новый ID класса")
        self.layout.addWidget(self.new_class_id_input)

        change_button = QPushButton("Изменить", self)
        change_button.clicked.connect(self.change_class)
        self.layout.addWidget(change_button)
        try:
            with open(file_path, 'r') as file:
                styles = file.read()
            self.setStyleSheet(styles)
        except FileNotFoundError:
            print("Файл стилей не найден.")
        except Exception as e:
            print(f"Ошибка при чтении файла стилей: {e}")
        self.setLayout(self.layout)


    def change_class(self):
        """Вызывается при нажатии на кнопку 'Изменить'."""
        try:
            change_id_product = int(self.product_id_input.text())
            new_id_class = int(self.new_class_id_input.text())

            self.db_dao.change_product_class(change_id_product, new_id_class)
            QMessageBox.information(self, "Успех", "Класс продукта успешно изменён.")
            self.close()
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Введите корректные числовые значения.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось изменить класс продукта: {str(e)}")
