# change_parent_class_window.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from code.constants import file_path


class ChangeParentClassWindow(QDialog):
    def __init__(self, parent, db_dao):
        super().__init__(parent)
        self.db_dao = db_dao
        self.setWindowTitle('Изменить родителя класса')
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        child_id_label = QLabel('ID класса:')
        self.child_id_input = QLineEdit()
        layout.addWidget(child_id_label)
        layout.addWidget(self.child_id_input)

        parent_id_label = QLabel('ID нового родителя:')
        self.parent_id_input = QLineEdit()
        layout.addWidget(parent_id_label)
        layout.addWidget(self.parent_id_input)

        change_button = QPushButton('Изменить')
        change_button.clicked.connect(self.change_parent_class)
        layout.addWidget(change_button)
        try:
            with open(file_path, 'r') as file:
                styles = file.read()
            self.setStyleSheet(styles)
        except FileNotFoundError:
            print("Файл стилей не найден.")
        except Exception as e:
            print(f"Ошибка при чтении файла стилей: {e}")
        self.setLayout(layout)

    def change_parent_class(self):
        try:
            child_id = int(self.child_id_input.text())
            parent_id = int(self.parent_id_input.text())
            self.db_dao.change_parent_class(child_id, parent_id)
            QMessageBox.information(self, 'Успех', 'Родитель класса изменен успешно')
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))
