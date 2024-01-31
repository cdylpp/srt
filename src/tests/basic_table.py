import sys
from typing import Optional
from pandas import DataFrame, read_csv
from PySide6.QtCore import Qt, QAbstractTableModel
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QTableView, QTableWidgetItem, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton)

DF = read_csv(r'../srt/datasets/Credentials.csv')

class DataView(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Data View")
        self.main_layout = QVBoxLayout(self)
        self.button_layout = QHBoxLayout(self)
        self.generate_button = QPushButton("Get Data")
        self.reset_button = QPushButton("Reset Table")
        self.button_layout.addWidget(self.generate_button)
        self.button_layout.addWidget(self.reset_button)

        self.data_table = DataWindow(df=DF)

        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.data_table)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        self.generate_button.clicked.connect(self.data_table.show)
        self.reset_button.clicked.connect(self.data_table.hide)


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
    
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
    
    def rowCount(self, index):
        return self._data.shape[0]
        
    def columnCount(self, index):
        return self._data.shape[1]
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

class DataWindow(QMainWindow):
    def __init__(self, df=None):
        super().__init__()
        self.table = QTableView()
        self.df = df

        self.model = TableModel(self.df)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)
        self.setGeometry(600, 100, 400, 200)
    

