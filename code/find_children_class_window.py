# find_children_window.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QListWidget

from code.constants import file_path


class FindChildrenWindow(QDialog):
    def __init__(self, parent, db_dao):
        super().__init__(parent)
        self.db_dao = db_dao
        self.setWindowTitle('Найти потомков класса')
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        class_id_label = QLabel('ID класса:')
        self.class_id_input = QLineEdit()
        layout.addWidget(class_id_label)
        layout.addWidget(self.class_id_input)

        find_button = QPushButton('Найти')
        find_button.clicked.connect(self.find_children)
        layout.addWidget(find_button)

        self.results_list = QListWidget()
        layout.addWidget(self.results_list)
        try:
            with open(file_path, 'r') as file:
                styles = file.read()
            self.setStyleSheet(styles)
        except FileNotFoundError:
            print("Файл стилей не найден.")
        except Exception as e:
            print(f"Ошибка при чтении файла стилей: {e}")

        self.setLayout(layout)

    def find_children(self):
        try:
            class_id = int(self.class_id_input.text())
            children = self.db_dao.find_children_by_class(class_id)
            self.results_list.clear()
            for child in children:
                self.results_list.addItem(f"ID: {child[0]}, Name: {child[1]}")
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))
