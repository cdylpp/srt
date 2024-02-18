# identify models
from data import DataGrabber, printResults
from classifiers import Classifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

MODELS = ['Logistic', 'KNN', 'Linear SVM', 'Kernel SVM', 'Gaussian Naive Bayes',
          'Decision Tree', 'Random Forest', 'XGBoost']
# get the data

df = pd.read_csv('datasets/student_data.csv', sep= ";")

clf = Classifier(df)
clf.set_params('Output', 0.25, remove='Enrolled')
clf.train()



def results(model: str):
    # Calculate the confusion matrix
    conf_matrix = clf.get_confusion(model)
    score = clf.get_score(model)
    print(score)
    # Plot confusion matrix as a heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=['Positive', 'Negative'], yticklabels=['True', 'False'])
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.show()


for model in MODELS:
    results(model)
