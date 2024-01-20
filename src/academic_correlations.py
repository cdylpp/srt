from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def import_data(file):
    try:
        df = pd.read_csv(file, sep=';')
        
    except Exception as e:
        print(e)
        
    return df 

def visualize_metric(student_data_file, metric, k='correlation'):
    # Load student data from CSV file
    student_df = pd.read_csv(student_data_file)

    # Separate features and target
    X = student_df.drop([metric], axis=1)
    y = student_df[metric]

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

    # Predict scores for the provided student data
    predictions = model.predict(X)

    # Check if 'prediction' column already exists before adding it
    if 'prediction' in student_df.columns:
        student_df = student_df.drop(['prediction'], axis=1)

    # Add the predictions to the student DataFrame
    student_df['prediction'] = predictions

    # Plotting based on the specified keyword
    if k == 'correlation':
        # Exclude non-numeric columns for correlation calculation
        numeric_student_df = student_df.select_dtypes(include=['int64', 'float64'])
        correlation_matrix = numeric_student_df.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title(f'Correlation Map for {metric}')
        plt.show()
    else:
        print(f'Unsupported keyword: {k}')

    return student_df

# Example usage:
csv_file_path = 'src/student_data.csv'
metric_to_visualize = 'RetentionScore'
visualize_metric(csv_file_path, metric_to_visualize)
