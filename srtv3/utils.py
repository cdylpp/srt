import re, os, csv
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


class HtmlParser:
    @staticmethod
    def get_headers(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.find_all(['h1', 'h2', 'h3'])



class Transformer:
    @staticmethod
    def headers(input_str):
        words = []
        current_word = ''

        for char in input_str:
            if char.isalpha():
                current_word += char
            elif current_word:
                words.append(current_word)
                current_word = ''

        if current_word:
            words.append(current_word)

        formatted_str = ' '.join(word.lower() for word in words)
        return formatted_str


class Validator:
    __valid_dict = {
        "email" : r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    }
    def __init__(self):
        return
        
    def validate(self, type, input):
        """Validates `input` for `type`"""
        pattern = self.__valid_dict[type]
        input = self.clean(input)
        return re.match(pattern, input) is not None
    
    def clean(self, s):
        return s.strip().lower()
    
# Test for validate()
# email = "example@email.com"
# if Validator().validate("email", email):
#     print("Valid email address")
# else:
#     print("Invalid email address")


# Test for clean()
# email = " ExAmplE@gmail.coM         "
# print(Validator().clean(email))
    



# # Test the function with examples
# print(format_headers("student_id"))            # Output: Student Id
# print(format_headers("Avg_Test_score"))        # Output: Avg Test Score
# print(format_headers("stUdy_hours-Per_Week"))  # Output: Study Hours Per Week


def detect_csv_separator(file_path):
    with open(file_path, 'r', newline='') as file:
        # Read a small portion of the file to infer the delimiter
        sample = file.read(8192)

        # Use the csv.Sniffer to automatically detect the delimiter
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
            return dialect.delimiter
        except csv.Error:
            print("Could not determine delimiter.")
            return None
        

# # Example usage
# file_path = 'datasets/student_data.csv'
# separator = detect_csv_separator(file_path)

# # Now, load the CSV file with the detected separator
# df = pd.read_csv(file_path, sep=separator)

# # Print the DataFrame
# print(df)
        
def path_to_title(file_path):
    """
    Convert a file path into a title by taking the last node.
    Handle underscores as spaces and Camel Case as separate words.
    """
    if not file_path:
        return None

    # Use os.path.basename to get the last component of the path
    title = os.path.basename(file_path)

    # Remove file extension, if any
    title, _ = os.path.splitext(title)

    # Replace underscores with spaces
    title = title.replace('_', ' ')

    # Split Camel Case into separate words
    title = ''.join([' ' + char.lower() if char.isupper() else char for char in title]).lstrip()

    return title

# # Example usage:
# file_path = "datasets/student_data_retention.csv"
# title = path_to_title(file_path)
# print(f"File Path: {file_path}")
# print(f"Title: {title}")

def filter_columns(df):
    categorical_cols = []
    numerical_cols = []
    
    for col in df.columns:
        if df[col].dtype in ('object', 'str', 'bool', 'category'):
            categorical_cols.append(col)
        elif df[col].dtype in ('int64', 'float64'):
            numerical_cols.append(col)
        else:
            print(f"Column '{col}' has an unsupported data type: {df[col].dtype}")
    
    return categorical_cols, numerical_cols

def value_to_text(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, (int, np.integer)):
        return str(value)
    elif isinstance(value, (float, np.floating)):
        return "{:.2f}".format(value)
    elif isinstance(value, (np.ndarray, np.generic)):
        return value.item()
    else:
        raise ValueError("Unsupported data type")
    
def variable_type(numpy_type):
    """
    Maps NumPy types to their corresponding string representations.

    Parameters:
    - numpy_type (type): The NumPy data type.

    Returns:
    - str: Continuous or Discrete.
    """
    if np.issubdtype(numpy_type, np.integer):
        return "discrete"
    elif np.issubdtype(numpy_type, np.floating):
        return "continuous"
    elif np.issubdtype(numpy_type, np.bool_):
        return "discrete"
    elif np.issubdtype(numpy_type, np.object_):
        return "discrete"  # Treat 'object' type as string
    else:
        return "Unknown"

def determine_visualization_type(data_type, uniqueness):
    """
    Determine the appropriate visualization type based on the data type and uniqueness.

    Parameters:
    - data_type (str): The type of data. Possible values are 'int', 'float', 'str', or 'bool'.
    - uniqueness (float): The level of uniqueness of the data. Possible values are 'very' or 'little'.

    Returns:
    - str: The type of visualization recommended based on the data type and uniqueness.
      Possible return values are 'continuous', 'discrete', 'pie', 'binary', or 'Unknown'.
      
    Note:
    - For 'int' or 'float' data types:
        - If uniqueness is 'very', the recommended visualization is 'continuous'.
        - If uniqueness is 'little', the recommended visualization is 'discrete'.
    - For 'str' data type:
        - If uniqueness is 'very', the recommended visualization is 'pie'.
        - If uniqueness is 'little', the recommended visualization is 'discrete'.
    - For 'bool' data type, the recommended visualization is 'binary'.
    - If the data type is unrecognized, the function returns 'Unknown'.
    """
    if data_type == "int" or data_type == "float":
        if uniqueness >= 0.50:
            return "continuous"
        else:
            return "discrete"
    elif data_type == "str":
        if uniqueness >= 0.50:
            return "pie"
        else:
            return "discrete"
    elif data_type == "bool":
        return "binary"
    else:
        return "Unknown"
    
def encode_categorical_column(df, column_name):
    """
    Encode categorical column of a DataFrame to numerical labels.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the categorical column.
        column_name (str): The name of the categorical column to encode.

    Returns:
        pd.DataFrame: A copy of the DataFrame with the categorical column transformed to numerical labels.
        dict: A dictionary mapping unique categorical values to numerical labels.
    """
    # Create a copy of the DataFrame to avoid modifying the original DataFrame
    df_encoded = df.copy()

    # Encode categorical column
    unique_categories = df_encoded[column_name].unique()
    encoded_map = {category: i for i, category in enumerate(unique_categories)}
    df_encoded[column_name] = df_encoded[column_name].map(encoded_map)

    return df_encoded[column_name], encoded_map

def encode_categorical_columns(df):
    """
    Encode categorical columns of a DataFrame to numerical labels.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the categorical columns.

    Returns:
        pd.DataFrame: A copy of the DataFrame with the categorical columns transformed to numerical labels.
        dict: A dictionary mapping unique categorical values to numerical labels for each encoded column.
    """
    # Create a copy of the DataFrame to avoid modifying the original DataFrame
    df_encoded = df.copy()
    
    # Identify columns with non-numeric data types (object or string)
    categorical_columns = df_encoded.select_dtypes(include=['object']).columns
    
    # Initialize an empty dictionary to store encoded mappings for each column
    encoded_maps = {}

    # Encode categorical columns
    for column_name in categorical_columns:
        unique_categories = df_encoded[column_name].unique()
        encoded_map = {category: i for i, category in enumerate(unique_categories)}
        df_encoded[column_name] = df_encoded[column_name].map(encoded_map)
        encoded_maps[column_name] = encoded_map

    return df_encoded, encoded_maps

# # Sample DataFrame
# data = {'Category': ['A', 'B', 'C', 'A', 'B', 'C', 'D'],
#         'Status': ['Active', 'Inactive', 'Active', 'Active', 'Inactive', 'Inactive', 'Active']}
# df = pd.DataFrame(data)

# # Encode categorical columns
# df_encoded, encoded_maps = encode_categorical_columns(df)

# print("Encoded DataFrame:")
# print(df_encoded)
# print("\nEncoded Maps:")
# print(encoded_maps)

def check_numerical_column(df, column_name):
    """
    Check if a column has numerical values.

    Parameters:
    - df: DataFrame, the input DataFrame.
    - column_name: str, the name of the column to check.

    Returns:
    - bool, True if the column has numerical values, False otherwise.
    """
    try:
        # Try converting the column to numerical type
        pd.to_numeric(df[column_name])
        return True
    except (ValueError, TypeError):
        # Column does not contain numerical values
        return False

def encode_categorical_columns(df):
    """
    Encode all columns of a DataFrame with categorical values to numerical values.

    Parameters:
    - df: DataFrame, the input DataFrame.

    Returns:
    - DataFrame, the DataFrame with categorical columns encoded to numerical values.
    """
    # Create a copy of the DataFrame to avoid modifying the original
    encoded_df = df.copy()

    # Iterate through each column
    for column_name in encoded_df.columns:
        if not check_numerical_column(encoded_df, column_name):
            # Encode non-numerical columns
            encoded_df[column_name] = pd.factorize(encoded_df[column_name])[0]

    return encoded_df



    
    
    