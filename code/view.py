from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidgetItem, QTableWidget
from PyQt5.QtGui import QFont


class TableView(QWidget):
    """Виджет для отображения данных в виде таблицы."""

    def __init__(self, data: list):
        """
        Конструктор класса.

        Параметры:
        - data (list): Двумерный список данных для отображения в таблице.
        """
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table_widget = QTableWidget()
        self.table_widget.setStyleSheet("QTableWidget { font-family: Arial; font-size: 12pt; }")
        self.layout.addWidget(self.table_widget)

    def update_data(self, data: list, column_names: list = None):
        """
        Обновляет данные в таблице.

        Параметры:
        - data (list): Двумерный список новых данных.
        - column_names (list, опционально): Список названий столбцов.
        """
        if not data:
            return

        num_rows = len(data)
        num_cols = len(data[0])

        self.table_widget.setRowCount(num_rows)
        self.table_widget.setColumnCount(num_cols)

        if column_names:
            self.table_widget.setHorizontalHeaderLabels(column_names)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.table_widget.setItem(row_idx, col_idx, item)
        scroll_bar = self.table_widget.verticalScrollBar()
        scroll_bar.setStyleSheet("""
                            QScrollBar:vertical {
                                border: none;
                                width: 14px;
                                margin: 15px 0 15px 0;
                            }
                            QScrollBar::handle:vertical {
                                background: gray;
        border-radius: 5px;
                                min-height: 30px;
                            }
                            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                                border: none;
                                background: none;
                            }

                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }
                        """)


