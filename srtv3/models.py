
import matplotlib
matplotlib.use('QtAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PyQt6.QtCore import QModelIndex, QObject, Qt, QAbstractTableModel, QAbstractItemModel, QVariant, pyqtSignal
from pandas import DataFrame
import matplotlib.pyplot as plt
plt.style.use("dark_background")

from utils import variable_type, encode_categorical_columns, HtmlParser, path_to_title
import pandas as pd
import markdown2
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix


class Classifier(QObject):

    modelsBuilt = pyqtSignal()
    def __init__(self, data: pd.DataFrame, remove: str = None) -> None:
        super().__init__()
        self.data = data
        self.target = None
        self.test_size = None
        self.models = {
            'Logistic': LogisticRegression(solver='liblinear'),
            'KNN': KNeighborsClassifier(n_neighbors=5, weights='distance'),
            'XGBoost': GradientBoostingClassifier(), 
            'Gaussian Naive Bayes': GaussianNB(),
            'Decision Tree': DecisionTreeClassifier(), 
            'Kernel SVM': SVC(kernel='rbf'), 
            'Linear SVM': SVC(kernel='linear'), 
            'Random Forest': RandomForestClassifier(max_depth=10)
        }
        self.classifiers = {}

    def set_params(self, target: str, test_size: float = .2, remove: str = None):
        self.target = target
        self.test_size = test_size
        if remove:
            self.remove(remove)

        self.X_train, self.X_test, self.y_train, self.y_test = self.split()

    def remove(self, value):
        """
        Removes the `value` from the target column.
        """
        self.data = self.data[self.data[self.target] != value]
        return

    def encode_target(self):
        if self.data[self.target].dtype == 'object':
            values = self.data[self.target].unique()
            mapping = {}
            for i, val in enumerate(values):
                mapping[val] = i

            self.data[self.target] = self.data[self.target].map(mapping)

    def split(self):
        self.encode_target()
        y, X = self.data[self.target], self.data.drop(self.target, axis=1)
        return train_test_split(X, y, test_size=self.test_size)

    def train(self):
        for name, model in self.models.items():
            clf = model.fit(self.X_train, self.y_train)
            self.classifiers[name] = clf

        self.modelsBuilt.emit()
        return

    def get_confusion(self, model: str):
        # return the confusion for the model type
        clf = self.classifiers[model]
        return confusion_matrix(self.y_test, clf.predict(self.X_test))

    def get_score(self, model: str) -> float:
        return self.classifiers[model].score(self.X_test, self.y_test)

    def get_info(self):
        # Dump model info
        pass
    

class TableModel(QAbstractTableModel):
    def __init__(self, data: DataFrame):
        super().__init__()
        self.cur_data = data
        self.queries = {("", ""): data}
    
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self.cur_data.iloc[index.row(), index.column()]
            return str(value)
    
    def rowCount(self, index):
        return self.cur_data.shape[0]
        
    def columnCount(self, index):
        return self.cur_data.shape[1]
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self.cur_data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self.cur_data.index[section])
    
    def sort(self, col_index, order):
        if order == Qt.SortOrder.AscendingOrder:
            ascending = True
        else:
            ascending = False
        column = self.cur_data.columns[col_index]
        self.cur_data.sort_values(by=[column], ascending=ascending, inplace=True)

    def filter(self, column, value):
        if (column, value) in self.queries.keys():
            self.cur_data = self.queries[(column, value)]
        else:
            filtered_df = self.cur_data[self.cur_data[column] == value]
            self.queries[(column, value)] = filtered_df
            self.cur_data = filtered_df
    
    def reset(self):
        self.cur_data = self.queries[("","")]


class SNSPlotter:
    """
    Model For Plotting, Updates the Figure and Canvas
    Types of Plots:
        'Distribution', 'Histogram', 'Box Plot', 'Scatter Plot',
        'Correlation Map'
    """

    @staticmethod
    def plot(data: pd.DataFrame, fig: Figure, canvas: FigureCanvasQTAgg, type: str, **kwargs):
        fig.clear()

        if 'x' in kwargs:
            column = kwargs['x']
            var_type = variable_type(data[column].dtype)

        if type == "Distribution":
            SNSPlotter().distribution(data, fig, var_type, **kwargs)

        elif type == "Box Plot":
            SNSPlotter().box_plot(data, fig, **kwargs)

        elif type == "Scatter Plot":
            SNSPlotter().scatter_plot(data, fig, var_type, **kwargs)

        elif type == "Correlation Map":
            SNSPlotter().corr_map(data, fig, **kwargs)

        else:
            print("Plot not offered, yet")

        canvas.draw()

    @staticmethod
    def distribution(data, fig, var_type, **kwargs):
        """
        Handle continuous and discrete distributions
        """
        if var_type == "discrete":
            kwargs['discrete'] = True
            sns.histplot(data, ax=fig.add_subplot(111), **kwargs)
            fig.axes[0].set_title(f"Distribution of {kwargs['x']}")
        else:
            sns.kdeplot(data, ax=fig.add_subplot(111), **kwargs)
            fig.axes[0].set_title(f"Kernel Density Estimate of {kwargs['x']}")
    
    @staticmethod
    def box_plot(data, fig, **kwargs):
        """
        Box plot for categorical data.
        """
        sns.boxplot(data, ax=fig.add_subplot(111), **kwargs)
        fig.axes[0].set_title(f"Box plot of {kwargs['x']}")

    @staticmethod
    def scatter_plot(data, fig, var_type, **kwargs):
        """
        Scatter plot for discrete and continuos data
        """
        if var_type == "discrete":
            # handle discrete scatter
            sns.stripplot(data, ax=fig.add_subplot(111), **kwargs)
            fig.axes[0].set_title(f"Swarm Plot of {kwargs['x']}")
            
        else:
            # handle continous scatter
            sns.scatterplot(data, ax=fig.add_subplot(111), **kwargs)
            fig.axes[0].set_title(f"Scatter Plot of {kwargs['x']}")
    
    @staticmethod
    def corr_map(data, fig, **kwargs):
        """
        Data wide correlation heat map
        """
        data = encode_categorical_columns(data)
        sns.heatmap(data.corr(), annot=False, cmap='coolwarm', linewidths=0.5, ax=fig.add_subplot(111))
    
    @staticmethod
    def confusion_matrix(conf_matrix, fig: Figure, canvas: FigureCanvasQTAgg, model: str, **kwargs):
        """
        Plots the confusion matrix for the prediction
        kwargs:
            - cmap: palette
            - xticklabels: 
            - yticklabels:
        """
        fig.clear()
        # Plot confusion matrix as a heatmap
        sns.heatmap(conf_matrix, annot=True, fmt="d", ax=fig.add_subplot(111), **kwargs)
        fig.axes[0].set_xlabel('Predicted labels')
        fig.axes[0].set_ylabel('True labels')
        fig.axes[0].set_title(f'Confusion Matrix for {model}')
        canvas.draw()


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
