from PyQt6 import QtWidgets

import pandas as pd
from utils import value_to_text, variable_type

from PyQt6.QtWidgets import (
    QApplication, QWidget, QCheckBox, QGroupBox, QButtonGroup, 
    QVBoxLayout, QMainWindow, QComboBox, QLabel, QTableView, QTreeWidget,
    QTreeWidgetItem, QHeaderView, QTabWidget, QHBoxLayout, QGridLayout, 
    QPushButton, QSlider)

from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from models import SNSPlotter

class ParameterComboBox(QComboBox):
    controlAndText = pyqtSignal(str, str)
    def __init__(self, parent: QWidget | None, param_type: str) -> None:
        super().__init__(parent)
        self.param_type = param_type
        self.currentTextChanged.connect(self.emit_control_signal)
    
    @pyqtSlot(str)
    def emit_control_signal(self, text):
        self.controlAndText.emit(self.param_type, text)


class PlotViewController(QWidget):
    """
    Visualization Tab
    Controls the plot view.
    """
    plot_clicked = pyqtSignal()

    def __init__(self, parent, data: pd.DataFrame, plotView):
        super().__init__(parent)
        self.type = "PlotView"
        self.df = data
        self.plotView = plotView
        self.plot_types = [
            '','Distribution','Histogram','Box Plot',
            'Scatter Plot', 'Correlation Map'
        ]
        self.palettes = ["", "rocket", "mako", "flare", "crest", "viridis", "plasma", "inferno", "magma", "cividis"]
        self.parameters = {"x":None, 
                           "y":None,
                           "hue":None,
                           "palette":None,
                           "col":None,
                           "discrete":None,
                           "fill":None
                           }
        self.controls = []
        self.init_ui()
    
    def init_ui(self):
        # choose `type`, choose `column`
        # dtype = get_dtype(`column`)
        # get widgets based on `type`, and `column`
        widgets = []

        plot_label = QLabel("Choose plot type:")
        self.plot_type = ParameterComboBox(self, "plot_type")
        self.plot_type.addItems(self.plot_types)
        self.plot_type.controlAndText.connect(self.update_parameters)
        widgets.append((plot_label, self.plot_type))
        self.controls.append(self.plot_type)

        x_label = QLabel("Choose x:")
        self.x = ParameterComboBox(self, "x")
        self.x.addItem("")
        self.x.addItems(self.df.columns)
        self.x.controlAndText.connect(self.update_parameters)
        widgets.append((x_label, self.x))
        self.controls.append(self.x)

        y_label = QLabel("Choose y:")
        self.y = ParameterComboBox(self, "y")
        self.y.addItem("")
        self.y.addItems(self.df.columns)
        self.y.controlAndText.connect(self.update_parameters)
        widgets.append((y_label, self.y))
        self.controls.append(self.y)

        hue_label = QLabel("Choose hue:")
        self.hue = ParameterComboBox(self, "hue")
        self.hue.addItem("")
        self.hue.addItems(self.df.columns)
        self.hue.controlAndText.connect(self.update_parameters)
        widgets.append((hue_label, self.hue))
        self.controls.append(self.hue)

        dim_label = QLabel("Choose column:")
        self.dim = ParameterComboBox(self, "col")
        self.dim.addItem("")
        self.dim.addItems(self.df.columns)
        self.dim.controlAndText.connect(self.update_parameters)
        widgets.append((dim_label, self.dim))
        self.controls.append(self.dim)

        palette_label = QLabel("Choose palette:")
        self.palette = ParameterComboBox(self, "palette")
        self.palette.addItems(self.palettes)
        self.palette.controlAndText.connect(self.update_parameters)
        widgets.append((palette_label, self.palette))
        self.controls.append(self.palette)

        fill_label = QLabel("Fill:")
        self.fill = ParameterComboBox(self, "fill")
        self.fill.addItems(['', 'Yes', 'No'])
        self.fill.controlAndText.connect(self.update_parameters)
        widgets.append((fill_label, self.fill))
        self.controls.append(self.fill)

        plot_button = QPushButton("Plot")
        plot_button.clicked.connect(self.on_plot_button)
        widgets.append(plot_button)

        reset_button = QPushButton("Reset Filters")
        reset_button.clicked.connect(self.on_reset_button)
        widgets.append(reset_button)

        # Create a vertical layout
        self.layout = QVBoxLayout()

        for w in widgets:
            if isinstance(w, tuple):
                label, widget = w
                row = QHBoxLayout()
                row.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)
                row.addWidget(widget, alignment=Qt.AlignmentFlag.AlignLeft)
                self.layout.addLayout(row)
            else:
                self.layout.addWidget(w)


        # Add a stretch to push widgets to the top
        self.layout.addStretch(1)

        self.setLayout(self.layout)
    
    
    @pyqtSlot()
    def on_plot_button(self):
        plot_type = self.plot_type.currentText()
        # get parameters
        kwargs = self.get_parameters()

        # pass to plot model to generate the plot
        figure, canvas = self.plotView.figure, self.plotView.canvas
        SNSPlotter.plot(self.df, figure, canvas, plot_type, **kwargs)
        self.plot_clicked.emit()
        return


    @pyqtSlot(str, str)
    def update_parameters(self, caller, text):
        if caller == "plot_type":
            return
        
        if caller == "fill":
            self.parameters[caller] = True if text == "Yes" else False
            return

        self.parameters[caller] = text
        return
    
    @pyqtSlot()
    def on_reset_button(self):
        # reset all the filters
        for control in self.controls:
            control.setCurrentIndex(0)
        return 
        

    def get_parameters(self):
        parms = {}
        for key, value in self.parameters.items():
            if value:
                parms[key] = value
        return parms


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
    

    @staticmethod
    def build_classifier_tree(parent, classifiers, stats):
        pass

class ControlDockTabWidget(QTabWidget):
    sort_selection = pyqtSignal(int, bool)
    filter_selection = pyqtSignal(int, str)

    def __init__(self, parent, df, table_view, plotView) -> None:
        super().__init__(parent)
        self.df = df
        self.table_view = table_view
        self.plotView = plotView
        self.plot_options = None

        # Tab Containers
        # Widgets go inside the containers
        self.controls_tab = QWidget()
        self.build_control_tab()

        self.insights_tab = QWidget()
        self.build_insight_tab()
        self.visualizations_tab = PlotViewController(self, self.df, plotView=self.plotView)

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
        nonunqiue_columns = [col for col in self.df.columns if self.df[col].nunique() < self.df[col].count()]
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
    
     
class ModellingController(QWidget):
    def __init__(self, parent: QWidget, data: pd.DataFrame) -> None:
        super().__init__(parent)
        self.data = data
        self.model_types = [
            '','All', 'Logistic', 'KNN', 'Linear SVM', 'Kernel SVM', 'Naive Bayes',
            'Decision Tree', 'Random Forest', 'XGBoost'
        ]
        self.init_ui()

    def init_ui(self):
        # Target Value
        target_label = QLabel("Select Target Variable:")
        target = ParameterComboBox(self, 'target')
        target.addItem("")
        target.addItems(self.data.columns)

        # Model Type
        model_label = QLabel("Select Model:")
        model = ParameterComboBox(self, 'model')
        model.addItems(self.model_types)

        # Train Test Split
        split_label = QLabel("Train / Test Split:")
        test_label = QLabel("Test")
        train_label = QLabel("Train")
        split_slider = QSlider(Qt.Orientation.Horizontal)
        split_slider.setMinimum(1)
        split_slider.setMaximum(99)
        split_slider.setValue(20)
        split_slider.valueChanged.connect(self.slider_value_changed)

        self.value_label = QLabel()

        prediction_button = QPushButton("Run Prediction")
        prediction_button.clicked.connect(self.run_prediction)
        reset_button = QPushButton("Reset Prediction")
        reset_button.clicked.connect(self.reset_parameters)

        row1 = QHBoxLayout()
        row1.addWidget(target_label, alignment=Qt.AlignmentFlag.AlignLeft)
        row1.addWidget(target, alignment=Qt.AlignmentFlag.AlignLeft)

        row2 = QHBoxLayout()
        row2.addWidget(model_label, alignment=Qt.AlignmentFlag.AlignLeft)
        row2.addWidget(model, alignment=Qt.AlignmentFlag.AlignLeft)

        row3 = QHBoxLayout()
        row3.addWidget(split_label, alignment=Qt.AlignmentFlag.AlignLeft)

        row4 = QHBoxLayout()
        row4.addWidget(test_label, alignment=Qt.AlignmentFlag.AlignLeft)
        row4.addWidget(split_slider, alignment=Qt.AlignmentFlag.AlignLeft)
        row4.addWidget(train_label, alignment=Qt.AlignmentFlag.AlignLeft)

        layout = QVBoxLayout()
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addLayout(row4)
        layout.addWidget(self.value_label)
        layout.addWidget(prediction_button)
        layout.addWidget(reset_button)

        layout.addStretch(1)

        self.setLayout(layout)


    def slider_value_changed(self, value):
        val = value / 100
        self.value_label.setText(f"Train: {1-val:.2f}, Test: {val:.2f}")
    
    def run_prediction(self):
        print("runnint prediction...")
        pass

    def reset_parameters(self):
        print("reset params")
        pass
        
        


