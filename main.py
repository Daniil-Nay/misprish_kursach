import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from code.controller import Controller


class MainWindow(QMainWindow):
    """Главное окно приложения."""

    def __init__(self):
        """Конструктор класса."""
        super().__init__()
        self.setWindowTitle("Курсовая работа")
        self.setFixedSize(1200, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = MainWindow()
    controller = Controller(root)
    root.show()
    sys.exit(app.exec_())
