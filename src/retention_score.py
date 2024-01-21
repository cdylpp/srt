from matplotlib import pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def generate_retention_score(student_data_file):
    # Load student data from CSV file
    student_df = pd.read_csv(student_data_file)

    # Separate features and target
    X = student_df.drop(['Retention_Score'], axis=1)
    y = student_df['Retention_Score']

    # Split the data for training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=13)

    # Define a column transformer to handle categorical and numerical data
    numerical_features = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X.select_dtypes(include=['object']).columns

    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    # Create a pipeline with preprocessing and linear regression model
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    # Fit the model on the training data
    model.fit(X_train, y_train)

    # Predict retention scores for the provided student data
    retention_predictions = model.predict(X)

    # Check if 'retention_prediction' column already exists before adding it
    if 'retention_prediction' in student_df.columns:
        student_df = student_df.drop(['retention_prediction'], axis=1)

    # Add the predictions to the student DataFrame
    student_df['retention_prediction'] = retention_predictions

    # Plotting actual vs predicted retention scores
    plt.scatter(student_df['Retention_Score'], student_df['retention_prediction'])
    plt.xlabel('Actual Retention Score')
    plt.ylabel('Predicted Retention Score')
    plt.title('Actual vs Predicted Retention Score')
    plt.tight_layout()
    plt.show()

    return student_df

# Example usage:
csv_file_path = 'src/student_data.csv'
predictions_df = generate_retention_score(csv_file_path)
print(predictions_df)
