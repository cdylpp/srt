import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

#TODO: Need better datasets
data = {
    'attendance': [90, 85, 95, 80, 70],
    'participation': [75, 80, 90, 85, 70],
    'extracurriculars': [3, 2, 4, 1, 5],
    'social_clubs': [2, 1, 3, 1, 4],
    'demerits': [1, 0, 2, 0, 3],
    'retention_score': [85, 90, 92, 80, 75]
}


df = pd.DataFrame(data)


class Predictor:
    def __init__(self, model=None):
        if model is None:
            self.model = LinearRegression()
        else:
            self.model = model
    
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)
    
    def evaluate(self, X_test, y_test):
        predictions = self.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        print(f'Mean Squared Error: {mse}')
        print(f'R-squared: {r2}')




def prep_data(df, target, test_size=0.2, random_state=13):
    X = df.drop(target, axis=1)
    y = df[target]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)




def test_predictor_class():
    X_train, X_test, y_train, y_test = prep_data(df, 'retention_score')
    predictor = Predictor(LinearRegression())

    predictor.train(X_train, y_train)
    predictor.evaluate(X_test, y_test)



test_predictor_class()