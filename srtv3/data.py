import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from prettytable import PrettyTable

def readCSVintoDF(file):
    df = pd.read_csv(file, sep=";")
    return df

class DataGrabber:
    data_paths = {'Retention':r'datasets/student_data.csv'}
    
    def __init__(self, data_set: str) -> None:
        self.file = self.data_paths[data_set]
        self.df = readCSVintoDF(self.file)
        
        self.data = np.array(self.df.values)
        n = len(self.data[0])
        self.X = [np.concatenate(([1], row[:n])) for row in self.data]
        self.target = [row[-1] for row in self.data]

    
    def train_test_split(self, test_size: float):
        return train_test_split(self.X, self.target, test_size=test_size)
    
def printResults(results):
    table = PrettyTable()
    table.field_names = ['Model Name', 'Accuracy', 'Confusion Matrix']

    for model_name, data in results.items():
        accuracy, matrix = data
        table.add_row([model_name, f'{accuracy:.2f}', str(matrix)])

    table.align["Model Name"] = "l"
    table.align["Accuracy"] = "c"
    table.align["Confusion Matrix"] = "r"

    print(table)

