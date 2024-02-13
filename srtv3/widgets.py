from PyQt6 import QtWidgets
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import pandas as pd
from utils import value_to_text

from PyQt6.QtWidgets import (
    QApplication, QWidget, QCheckBox, QGroupBox, QButtonGroup, 
    QVBoxLayout, QMainWindow, QComboBox, QLabel, QTableView, QTreeWidget,
    QTreeWidgetItem, QHeaderView, QTabWidget, QHBoxLayout)

from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from models import TableModel, DataFramePlotter, MplCanvas

class FilterWidget(QWidget):
    def __init__(self, column_header, choices):
        super().__init__()
        self.column_header = column_header
        self.choices = choices
        self.init_uit()

    def init_uit(self):
        """Set up the application's GUI."""
        self.setup_widget()
        self.show()

    def setup_widget(self):
        """Create and arrange widgets in the main window."""
        self.tristate_cb = QCheckBox("All")
        self.tristate_cb.stateChanged.connect(self.show_state)
        self.tristate_cb.stateChanged.connect(self.updateTristateCb)

        # Create the check boxes with an indentation
        # using style sheets
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(False)
        gb_v_box = QVBoxLayout()
        gb_v_box.addWidget(self.tristate_cb)
        for choice in self.choices:
            check_box = QCheckBox(choice)
            check_box.stateChanged.connect(self.show_state)
            check_box.setStyleSheet("padding-left: 10px")
            self.button_group.addButton(check_box)
            gb_v_box.addWidget(check_box)

        self.button_group.buttonToggled.connect(self.checkButtonState)
        gb_v_box.addStretch()

        group_box = QGroupBox(self.column_header)
        group_box.setLayout(gb_v_box)

        main_v_box = QVBoxLayout()
        main_v_box.addWidget(group_box)
        self.setLayout(main_v_box)

    def updateTristateCb(self, state):
        """Use the QCheckBox to check or uncheck all boxes."""
        for button in self.button_group.buttons():
            if state == 2: # Qt.CheckState.Checked
                button.setChecked(True)
            elif state == 0: # Qt.CheckState.Unchecked
                button.setChecked(False)
    
    def checkButtonState(self, button, checked):
        """Determine which buttons are selected and set the state
        of the tri-state QCheckBox."""
        button_states = []

        for button in self.button_group.buttons():
            button_states.append(button.isChecked())

        if all(button_states):
            self.tristate_cb.setCheckState(Qt.CheckState.Checked)
            self.tristate_cb.setTristate(False)
        elif any(button_states) == False:
            self.tristate_cb.setCheckState(Qt.CheckState.Unchecked)
            self.tristate_cb.setTristate(False)
        else:
            self.tristate_cb.setCheckState(Qt.CheckState.PartiallyChecked)
    
    def show_state(self, s):
        print(Qt.CheckState(s) == Qt.CheckState.Checked)
        print(s)

class ComboBox(QWidget):
    def __init__(self, parent: QWidget, title, choices):
        super().__init__(parent)
        self.title = title
        self.filters = choices
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel(self.title))
        self.filter_box = QComboBox(self)
        self.filter_box.addItems(self.filters)
        self.layout.addWidget(self.filter_box)
        self.filter_box.currentIndexChanged.connect(self.index_changed)
        self.filter_box.currentTextChanged.connect(self.text_changed)

    def index_changed(self, i):
        print(i)

    def text_changed(self, s):
        print(s)

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


        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addLayout(h_box)
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def plot_dist(self, column_header, plot_type='histogram', **kwargs):
        """
        Plot the distribution of a specified column in the DataFrame.

        Parameters:
            column_header (str): The name of the column to plot.
            plot_type (str, optional): Type of plot to create. Defaults to 'histogram'
            **kwargs: Additional keyword args to pass to the plot function
        """
        if self.df is None:
            print("No DataFrame provided.")
            return
        
        column_data = self.df[column_header]
        DataFramePlotter.plot_dist(self.canvas, column_data, plot_type, **kwargs)
    
    def plot_continuous_distribution(self, column_header):
        
        if self.df is None:
            print("No DataFrame is provided")
            return
        
        data = self.df[column_header]
        mean, std, max, min, count = (data.mean(), data.std(), data.max(), data.min(), data.count())
        DataFramePlotter.plot_continuous_distribution(self.canvas, column_header, mean, std, max, min, count)

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

class CustomTableView(QTableView):

    def __init__(self, parent: QWidget, model) -> None:
        super().__init__(parent)
        self.type = "TableView"
        self.setModel(model)

    def sortByColumn(self, column: int, order: Qt.SortOrder) -> None:
        return super().sortByColumn(column, order)
    
    def selectColumn(self, column):
        return super().selectColumn(column)

class TableWidget(QWidget):
    def __init__(self, df=None):
        super().__init__()
        
        # Create the table view
        self.table = QTableView()
        
        # Set the DataFrame
        self.df = df
        
        # Create the model and set it to the table view
        self.model = TableModel(self.df)
        self.table.setModel(self.model)
        
        # Create a layout and add the table view to it
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        
        # Set the layout for the widget
        self.setLayout(layout)

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
    sort_selection = pyqtSignal(int)

    def __init__(self, parent, df) -> None:
        super().__init__(parent)
        self.df = df

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
    
    def build_control_tab(self):
        v_box = QVBoxLayout()
        

        label = QLabel("Sort by: ")
        sort_by = QComboBox(self.controls_tab)
        sort_by.addItems(self.df.columns)
        sort_by.currentIndexChanged.connect(self.on_sort_selection)

        h_box = QHBoxLayout()
        h_box.addWidget(label)
        h_box.addWidget(sort_by)

        sort_order = QCheckBox(self.controls_tab)
        sort_order.setText("Ascending")
        sort_order.setChecked(True)
        sort_order.stateChanged.connect(self.toggle_sort_order)

        v_box.addLayout(h_box)
        v_box.addWidget(sort_order)

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
        """
        emit the sort_selection with index
        """
        # select table by col
        self.sort_selection.emit(col_idx)
        print(f"sort by: {col_idx}")
        pass

    @pyqtSlot(int)
    def toggle_sort_order(self, on):
        if on:
            print("state on")
        else:
            print("state off")

    def sort(self):
        pass



