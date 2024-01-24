import mysql.connector
import csv
from PyQt6.QtWidgets import QMessageBox

# Config for AWS database, don't change
DB_CONFIG = {
    'host': "srt-database-1.cve60ywu8ysv.us-west-1.rds.amazonaws.com",
    'user': 'srtAdmin',
    'password': 'Bubmi1-xynvez-kijpuv',
    'database': 'srtdatabase'
}


def csv_to_dict(file_path):
    """Takes a file_path and returns a list of dicts whose key is `username`"""
    rows = []
    with open(file_path, 'r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            rows.append(dict(row))
    return rows

def generate_credential_dict(data_tuple):
    """
    Returns a dict object with `data_tuple` as the values for the keys
    Example:
        generate_credential_dict(('1', 'joesmith', 'joe1', 'admin', 'Joe', 'Smith', 'joe.smith@mail.com'))
        >>> {'id': '1', 'username': 'joesmith', 'password': 'joe1', 'role': 'admin', 'first_name': 'Joe', 'last_name': 'Smith', 'email': 'joe.smith@mail.com'}
    Args:
        data_tuple (Tuple): a tuple of data fields from the credentials database

    Returns:
        dict[str, str]: with headers (e.g. 'id', 'username'...) as keys.
    """
    field_names = ['id', 'username', 'password', 'role', 'first_name', 'last_name', 'email']
    data_dict = {field: value for field, value in zip(field_names, data_tuple)}
    return data_dict
    

class DatabaseManager:
    def __init__(self,type,**kwargs):
        self.type = type
        self.db = self.connect(**kwargs)
    
    def fetch(self,field: str,target: str) -> dict[str, str]:
        """
        Fetches the `target` from the `field` column from the database.
        
        Args:
            field (str): valid attribute within the database (e.g., id, password...)
            target (str): value to look for in the database 

        Returns:
            dict[str, str]: if `target` is found it returns the whole row as a dict. Else None
        """
        
        if self.type == 'csv':
            # handle csv case
            return
        
        elif self.type == 'mysql':
            # handle mysql case
            cursor = self.db.cursor()
            query = "SELECT * FROM admin_credentials WHERE %s = %s"
            cursor.execute(query, (field, target))
            result = cursor.fetchone()
            cursor.close
            if result:
                return generate_credential_dict(result)
            else:
                return None
    
    def connect(self, **kwargs):
        if self.type == "mysql":
            return mysql.connector.connect(**kwargs)
        if self.type == "csv":
            return csv_to_dict(kwargs['file'])

    def close_connection(self):
        if self.type == 'mysql':
            if self.db_connection.is_connected():
                self.db_connection.close()
    
    def login(self, username, password):
        """
        Login to Database with `username` and `password`
        
        Raises ValueError for invalid password.
        Raises KeyError if username is not found.
        """
        # csv login method
        if self.type == "csv":
            for user in self.db:
                if user['username'] == username:
                    if user['password'] == password:
                        return True
                    else:
                        return False

            raise KeyError(f"{username} not in {self.file_name}")
                
        
        # mysql login method 
        elif self.type == "mysql":
            cursor = self.db.cursor()
            #to check login
            query = "SELECT * FROM admin_credentials WHERE BINARY username = %s AND BINARY password = %s"
            cursor.execute(query, (username, password))

            user = cursor.fetchone()

            cursor.close()

            if user:
                return True
            else:
                return False
    
    def getCredentials(self, username):
        """returns credientials for `username`"""

        # returns the entire dict for username in csv file
        if self.type == "csv":
            for user in self.db:
                if user['username'] == username:
                    return user
            raise KeyError(f"{username} not in {self.file_name}")

        # returns row with username == `username` as a dict object
        elif self.type == "mysql":
            cursor = self.db.cursor()
            query = "SELECT * FROM admin_credentials WHERE username = %s"
            cursor.execute(query, (username,))
            data = cursor.fetchone()
            cursor.close()
            return generate_credential_dict(data)





