import sys
from typing import Optional
from pandas import DataFrame, read_csv
from PySide6.QtCore import Qt, QAbstractTableModel
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QTableView, QTableWidgetItem, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton)

from utils import format_headers

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
                return format_headers(str(self._data.columns[section]))

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

class DataWindow(QMainWindow):
    def __init__(self, df=None, **kwargs):
        super().__init__()
        self.table = QTableView()
        self.df = df

        if 'title' in kwargs:
            self.setWindowTitle(kwargs['title'])

        self.model = TableModel(self.df)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)
    

