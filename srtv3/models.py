
import matplotlib
matplotlib.use('QtAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PyQt6.QtCore import QModelIndex, QObject, Qt, QAbstractTableModel, QAbstractItemModel, QVariant
from pandas import DataFrame
import matplotlib.pyplot as plt
plt.style.use("dark_background")

from utils import map_numpy_type_to_string, encode_categorical_column, HtmlParser, path_to_title
import numpy as np
import pandas as pd
import markdown2
    
class TableModel(QAbstractTableModel):
    def __init__(self, data: DataFrame):
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
    
    def sort(self, col_index, order):
        if order == Qt.SortOrder.AscendingOrder:
            ascending = True
        else:
            ascending = False
        column = self._data.columns[col_index]
        self._data.sort_values(by=[column], ascending=ascending, inplace=True)
    


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)


class DataFramePlotter:
    @staticmethod
    def plot(canvas, column, data, type, legend):
        # Ensure the Layout remains the same
        ax = canvas.axes
        ax.clear()
        dtype = map_numpy_type_to_string(data[column].dtype)

        if type == "Distribution":
            x = data[column]
            if dtype == "float":
                mean, std, max, min, count = (x.mean(), x.std(), x.max(), x.min(), x.count())
                x = np.random.normal(loc=mean, scale=std, size=count)

                n, bins, patches = ax.hist(x, bins=count//10, density=True)
                
                x = np.linspace(min, max, 100)
                p = ((1 / (np.sqrt(2 * np.pi) * std)) * np.exp(-0.5 * (1 / std * (bins - mean))**2))
                ax.plot(bins, p, '--')
                ax.set_xlabel('Values')
                ax.set_ylabel('Probability density')
                ax.set_title('Histogram of normal distribution: 'fr'$\mu={mean:.0f}$, $\sigma={std:.0f}$')
            
            elif dtype == "int":
                ax.hist(x)
                ax.set_title("Discrete Distribution")
                ax.set_ylabel("Frequency")
                ax.set_xlabel("Values")

            else:
                encoded_column, map = encode_categorical_column(data, column)

                print(encoded_column)
                counts, bins = np.histogram(encoded_column)
                ax.stairs(counts, bins, fill=True)
                labels = list(map.keys())
                values = list(map.values())
                pos = np.arange(len(labels))

                ax.set_xticks(pos, labels)
                ax.set_title("Categorical Distributions")
                ax.set_ylabel("Frequency")
                ax.set_xlabel("Values")

        # elif type == "Pie Chart":
        #     if dtype in ('int', 'float'):
        #         print(f"Chart type with {dtype} not supported")
        #         pass

        #     else:
        #         # make pie chart
        #         x = data[column].value_counts()
        #         colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))
        #         ax.pie(x, colors=colors, radius=3, center=(4,4),
        #             wedgeprops={"linewidth": 1, "edgecolor":"white"}, frame=True)
                
        #         ax.set(xlim=(0,8), xticks=np.arange(1,8),
        #             ylim=(0,8), yticks=np.arange(1,8))
        #         ax.set_title("Pie Chart")


        else:
            print("Plot type not supported yet.")
        
        if legend:
            ax.legend()
            
        ax.grid(False)
        canvas.draw()

    @staticmethod
    def plot_dist(canvas, column_data, plot_type='histogram', **kwargs):
        ax = canvas.axes
        ax.clear()
        if plot_type == 'histogram':
            ax.hist(column_data, **kwargs)
        elif plot_type == 'line':
            ax.plot(column_data, **kwargs)
        elif plot_type == 'KDE':
            column_data.plot(kind='kde', ax=ax, **kwargs)
        elif plot_type == 'boxplot':
            column_data.plot(kind='box', ax=ax, **kwargs)
        else:
            print("Unsupported plot_type. Supported types are: histogram, line, KDE, boxplot.")
        
        ax.set_title('Distribution')
        ax.set_ylabel('Frequency' if plot_type in ('histogram', 'KDE') else 'Value')
        ax.grid(False)
        canvas.draw()

    @staticmethod
    def plot_continuous_distribution(canvas, title, mean, std, max_val, min_val, count):
        # Generate random samples from a normal distribution
        ax = canvas.axes
        ax.clear()
        data = np.random.normal(loc=mean, scale=std, size=count)
        ax.hist(data, bins=30, density=True, alpha=0.6, color='b') # TODO: Algorithm for bin setting
        
        # Plot density curve
        xmin, xmax = min_val, max_val
        x = np.linspace(xmin, xmax, 100)
        p = (1/(std * np.sqrt(2 * np.pi))) * np.exp(-((x - mean) ** 2) / (2 * std ** 2))
        ax.plot(x, p, 'g', linewidth=2)

        # Add labels and title
        ax.set_xlabel('Value')
        ax.set_ylabel('Density')
        ax.set_title(f'Continuous Distribution: {title}')

        canvas.draw()


class TreeItem:
    def __init__(self, data, parent=None) -> None:
        self.data = data
        self.parent = parent
        self.children = []

    def data(self, column):
        """
        return the data value for the given column index
        """
        if column >= 0 and column < len(self.data):
            return self.data[column]
        return None
    
    def set_data(self, column, value):
        if column >= 0 and column < len(self.data):
            self.data[column] = value
    
    def parent(self):
        return self.parent
    
    def child(self, row):
        if row >= 0 and row < len(self.children):
            return self.chidlern[row]
        return None
    
    def child_count(self):
        return len(self.children)
    
    def column_count(self):
        return len(self.data)
    
    def append_child(self, item):
        self.children.append(item)
    

class MarkdownModel:
    def __init__(self, file_path) -> None:
        self.file_path = file_path # path to markdown file.
        self._html_parser = HtmlParser()
        self.html_content = None
        self.title = None

        self.set_title()
        self.set_html_content()
        

    def set_html_content(self):
        markdown_content = self.load_markdown_file(self.file_path)
        self.html_content = markdown2.markdown(markdown_content)
        return self.html_content

    def load_markdown_file(self, file_path):
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                markdown_content = file.read()

        return markdown_content

    def set_title(self):
        self.title = path_to_title(self.file_path)
        return

    def headers(self):
        return self._html_parser.get_headers(self.html_content)


class TreeModel(QAbstractItemModel):
    def __init__(self, data, parent=None) -> None:
        super().__init__(parent)
        self.rootItem = TreeItem([])
        self.setupModelData(data, self.rootItem)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        if role != Qt.ItemDataRole.DisplayRole:
            return QVariant()
        
        item = index.internalPointer()
        return item.data(index.column())
    
    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return super().flags(index)
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        return super().headerData(section, orientation, role)
    
    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        
        parentItem = self.rootItem if not parent.isValid() else parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        return QModelIndex()
    
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem == self.rootItem:
            return QModelIndex()
        
        return self.createIndex(parentItem.row(), 0, parentItem)
    
    def rowCount(self, parent: QModelIndex = ...) -> int:
        parentItem = self.rootItem if not parent.isValid() else parent.internalPointer()
        return parentItem.child_count()
    
    def columnCount(self, parent: QModelIndex = ...) -> int:
        parentItem = self.rootItem if not parent.isValid() else parent.internalPointer()
        return parentItem.column_count()
    
    def setupModelData(self, data, parent):
        for element in data:
            if isinstance(element, str):
                itemData = [element, ""]
                newItem = TreeItem(itemData, parent)
                parent.appendChild(newItem)
            elif isinstance(element, list):
                if parent.child_count() > 0:
                    currentParent = parent.child(parent.child_count() - 1)
                    self.setupModelData(element, currentParent)