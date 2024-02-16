from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import CategoricalNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from typing import List

class Classifier:
    models = {'Logistic': LogisticRegression(),'KNN':KNeighborsClassifier(n_neighbors=5),
              'XGBoost':GradientBoostingClassifier(), 'Naive Bayes':CategoricalNB(),
              'Decision Tree':DecisionTreeClassifier(), 'Kernel SVM':SVC(kernel='rbf'), 
              'Linear SVM':SVC(kernel='linear'), 'Random Forest':RandomForestClassifier(n_estimators=10)}
    
    def __init__(self, X: List[List], y: List[float], model: str) -> None:
        self.X_train = X
        self.y_train = y
        self.model = self.models[model].fit(self.X_train, self.y_train)