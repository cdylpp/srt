from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from pandas import DataFrame


class Classifier:
    def __init__(self, data: DataFrame, remove: str = None) -> None:
        self.data = data # data frame with all data -> [X y]
        self.target = None # Target column or feature to classify
        self.test_size = None 
        self.labels = None # Labels of the target class
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
            self.labels = self.data[self.target].unique()
            mapping = {}
            for i, val in enumerate(self.labels):
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