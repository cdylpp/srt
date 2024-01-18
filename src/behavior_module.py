import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

data = {
    'attendance': [90, 85, 95, 80, 70],
    'participation': [75, 80, 90, 85, 70],
    'extracurriculars': [3, 2, 4, 1, 5],
    'social_clubs': [2, 1, 3, 1, 4],
    'demerits': [1, 0, 2, 0, 3],
    'retention_score': [85, 90, 92, 80, 75]
}

df = pd.DataFrame(data)

X = df.drop('retention_score', axis=1)
y = df['retention_score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=13)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

plt.scatter(y_test, y_pred)
plt.xlabel('Actual Retention Score')
plt.ylabel('Predicted Retention Score')
plt.title('Actual vs Predicted Retention Score')
plt.show()


