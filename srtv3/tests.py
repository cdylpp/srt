# identify models
from data import DataGrabber, printResults
from classifiers import Classifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd

MODELS = ['Logistic', 'KNN', 'Linear SVM', 'Kernel SVM', 'Naive Bayes',
          'Decision Tree', 'Random Forest', 'XGBoost']
# get the data

df = pd.read_csv('datasets/student_data.csv', sep= ";")
mapping = {'Graduate':2, 'Enrolled':1, "Dropout":0}
df['Output'] = df['Output'].map(mapping)

y = df['Output']
X = df.drop('Output', axis=1)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

classifiers = {}
# Build / train classifiers for model in MODELS:
for model in MODELS:
    classifiers[model] = Classifier(X_train, y_train, model)

# Test each model
metrics = [accuracy_score, confusion_matrix]
results = {}
for model, clf in classifiers.items():
    y_test_pred = clf.model.predict(X_test)
    results[model] = [metric(y_test, y_test_pred) for metric in metrics]
    
# Show the results
printResults(results)