from PyQt6 import QtWidgets
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import pandas as pd
from utils import value_to_text

from PyQt6.QtWidgets import (
    QApplication, QWidget, QCheckBox, QGroupBox, QButtonGroup, 
    QVBoxLayout, QMainWindow, QComboBox, QLabel, QTableView, QTreeWidget,
    QTreeWidgetItem, QHeaderView, QTabWidget, QHBoxLayout, QGridLayout, QPushButton)

from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from models import DataFramePlotter, MplCanvas



class PandasPlotter(QWidget):
    def __init__(self, parent=None, df=None):
        super().__init__(parent)
        self.df = df
        self.plot_types = [
            'Distribution','Scatter Plot','Box Plot', 'Line Plot',
            'Heatmap', 'Bar Plot', 'Violin Plot', 'Pie Chart', 'Area Plot',
            'Stacked Bar Plot', 'Bubble Chart', 'Correlation Plot'
        ]
        self.init_ui()
    
    def init_ui(self):
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        h_box = QHBoxLayout()

        pt_label = QLabel("Plot type:",self)
        self.plot_type = QComboBox(self)
        self.plot_type.setToolTip("Select plot type")
        self.plot_type.addItems(self.plot_types)
        self.plot_type.currentTextChanged.connect(self.on_plot_selection)

        col_label = QLabel("Column:",self)
        self.columns = QComboBox(self)
        self.columns.setToolTip("Select column")
        self.columns.addItems(self.df.columns)
        self.columns.currentTextChanged.connect(self.on_column_selection)

        self.legend_checkbox = QCheckBox(self)
        self.legend_checkbox.setText("Show Legend")
        self.legend_checkbox.setChecked(True)
        self.legend_checkbox.stateChanged.connect(self.on_legend_toggle)

        h_box.addWidget(pt_label)
        h_box.addWidget(self.plot_type)
        h_box.addWidget(col_label)
        h_box.addWidget(self.columns)
        h_box.addWidget(self.legend_checkbox)

        layout = QVBoxLayout()
        layout.addLayout(h_box)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    

    def visualize(self, column_header, plot_type):
        data = self.df[column_header]
        DataFramePlotter.plot(self.canvas, column_header, data, plot_type)


    @pyqtSlot(str)
    def on_plot_selection(self, txt):
        print(f"plot type chosen: {txt}")
        self.plot()
    

    @pyqtSlot(str)
    def on_column_selection(self, txt):
        print(f"column chosen: {txt}")
        self.plot()


    @pyqtSlot()
    def on_legend_toggle(self):
        if self.legend_checkbox.isChecked():
            print("Show Legend")
        else:
            print("Hide Legend")


    def plot(self):
        plot_type = self.plot_type.currentText()
        column = self.columns.currentText()
        legend = self.legend_checkbox.isChecked()
        DataFramePlotter.plot(self.canvas, column, self.df, plot_type, legend)





class TableView(QTableView):
    def __init__(self, parent: QWidget, model) -> None:
        super().__init__(parent)
        self.type = "TableView"
        self.model = model
        self.setModel(model)

    def sortByColumn(self, column: int, order: Qt.SortOrder) -> None:
        return super().sortByColumn(column, order)
    
    def selectColumn(self, column):
        return super().selectColumn(column)
    
    def filterBy(self, column, value):
        self.model.filter(column, value)
        self.setModel(self.model)

    def resetFilter(self):
        self.model.reset()
        self.setModel(self.model)

    def horizontalHeader(self) -> QHeaderView | None:
        return super().horizontalHeader()


class TreeWidgetFactory():
    @staticmethod
    def build_tree(parent,data: pd.DataFrame):
        tree = QTreeWidget(parent)
        tree.setHeaderLabels(('Measure', 'Type', 'Value'))
        tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        # Sperate the numerical data verus the categorical data.
        # categorical_cols, numerical_cols = filter_columns(data)

        # Create parents
        parents = {}
        for attr in data.columns:
            dtype = str(data[attr].dtype)
            parent = QTreeWidgetItem(tree, [attr, dtype, ""])
            parents[attr] = parent

        # Create childern
        summary = data.describe(include='all')

        for attr in data.columns:
            for stat in summary.T.columns:
                if str(summary.at[stat, attr]) != 'nan':
                    val = value_to_text(summary.at[stat, attr])
                    parents[attr].addChild(QTreeWidgetItem([stat, "", val]))
        
        return tree
    
    @staticmethod
    def build_html_tree(parent, headers):
        tree = QTreeWidget(parent)
        tree.setColumnCount(1)  # Set the number of columns
        stack = []
        top_level = None

        for header in headers:
            # Get the tag name and text content of the header
            tag = header.name
            text = header.text.strip()
            
            # Check if the stack is empty or the tag name is greater than or equal to the top of the stack
            if not stack or tag >= stack[-1][0]:
                stack.append([tag, text])
                if top_level:
                    item = QTreeWidgetItem(top_level)
                else:
                    item = QTreeWidgetItem(tree)
                item.setText(0, text)

                if tag == 'h2':
                    top_level = item
                    
            else:
                while stack and tag < stack[-1][0]:
                    stack.pop()
                    top_level = top_level.parent() if top_level else None
                # Push the tag name and the text content as a list to the stack
                stack.append([tag, text])
                # If there's a parent, set it as the current item
                if top_level:
                    item = QTreeWidgetItem(top_level)
                else:
                    item = QTreeWidgetItem(tree)
                item.setText(0, text)
                # If the tag is h2, update the parent
                if tag == 'h2':
                    top_level = item
        return tree


class ControlDockTabWidget(QTabWidget):
    sort_selection = pyqtSignal(int, bool)
    filter_selection = pyqtSignal(int, str)

    def __init__(self, parent, df, table_view) -> None:
        super().__init__(parent)
        self.df = df
        self.table_view = table_view

        # Tab Containers
        # Widgets go inside the containers
        self.controls_tab = QWidget()
        self.build_control_tab()

        self.insights_tab = QWidget()
        self.build_insight_tab()
        self.visualizations_tab = QWidget()

        self.addTab(self.controls_tab, 'Controls')
        self.addTab(self.insights_tab, 'Insights')
        self.addTab(self.visualizations_tab, 'Visualizations')

        self.setDocumentMode(True)
        self.setTabPosition(QTabWidget.TabPosition.North)
    
    def build_control_tab(self):
        v_box = QVBoxLayout()
        grid_layout = QGridLayout()
        
        # Label, ComboBox, Order, Button
        sort_label = QLabel("Sort by:")
        self.sort_by = QComboBox(self.controls_tab)
        self.sort_by.addItems(self.df.columns)
        self.sort_by.currentIndexChanged.connect(self.on_sort_selection)

        self.sort_order = QCheckBox(self.controls_tab)
        self.sort_order.setText("Ascending")
        self.sort_order.setChecked(True)

        sort_button = QPushButton( "Sort", self.controls_tab)
        sort_button.clicked.connect(self.on_sort_button)

        grid_layout.addWidget(sort_label, 0, 0, Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(self.sort_by, 0, 1, Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(self.sort_order, 1, 0, Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(sort_button, 1, 1, Qt.AlignmentFlag.AlignCenter)

        # Filter Label, Combo, Combo, Button
        filter_label = QLabel("Filter by:")
        self.filter_by = QComboBox(self.controls_tab)
        values_label = QLabel("Filter values:")
        self.filter_values = QComboBox(self.controls_tab)
        filter_button = QPushButton("Filter", self.controls_tab)
        filter_button.clicked.connect(self.on_filter_button)
        self.reset_filter = QPushButton("Reset Filter", self.controls_tab)
        self.reset_filter.clicked.connect(self.on_reset_filter)

        # Only show columns that have a uniquessnes score of less than 1
        nonunqiue_columns = [col for col in self.df.columns if self.df[col].nunique() / self.df[col].count() < 1]
        self.filter_by.addItems(nonunqiue_columns)
        self.filter_by.currentTextChanged.connect(self.on_filter_by) # change the variable list for the unique

        grid_layout.addWidget(filter_label, 2, 0, Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(self.filter_by, 2, 1, Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(values_label, 3, 0, Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(self.filter_values, 3, 1, Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(filter_button, 4, 0, Qt.AlignmentFlag.AlignLeft)
        grid_layout.addWidget(self.reset_filter, 4, 1, Qt.AlignmentFlag.AlignLeft)

        

        v_box.addLayout(grid_layout)

        self.controls_tab.setLayout(v_box)
        
    def build_insight_tab(self):
        v_layout = QVBoxLayout()
        self.measures_tree = TreeWidgetFactory().build_tree(self.insights_tab, self.df)
        v_layout.addWidget(self.measures_tree)
        self.insights_tab.setLayout(v_layout)
        
    def build_viz_tab(self):
        pass
    
    @pyqtSlot(int)
    def on_sort_selection(self, col_idx):
        self.table_view.selectColumn(col_idx)

    @pyqtSlot()
    def on_sort_button(self):
        # get sort parameters
        # execute sort algorithm
        order = Qt.SortOrder.AscendingOrder if self.sort_order.isChecked() else Qt.SortOrder.DescendingOrder
        col_idx = self.sort_by.currentIndex()
        self.table_view.sortByColumn(col_idx, order)

    @pyqtSlot(str)
    def on_filter_by(self, col):
        self.filter_values.clear()
        values = [str(val) for val in self.df[col].unique()]
        self.filter_values.addItems(values)

    @pyqtSlot()
    def on_filter_button(self):
        # get filter parameters
        # send filter item to the TableView
        col_idx = self.filter_by.currentText()
        value = self.filter_values.currentText()
        self.table_view.filterBy(col_idx, value)

    def on_reset_filter(self):
        self.table_view.resetFilter()




