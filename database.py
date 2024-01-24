import mysql.connector
import csv
from PyQt6.QtWidgets import QMessageBox

DB_CONFIG = {
    'host': "srt-database-1.cve60ywu8ysv.us-west-1.rds.amazonaws.com",
    'user': 'srtAdmin',
    'password': 'Bubmi1-xynvez-kijpuv',
    'database': 'srtdatabase'
}

def csv_to_dict(file_path):
    """Returns a CSV file as a list of key value pairs"""
    rows = []
    with open(file_path, 'r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            rows.append(dict(row))
    return rows

def generate_credential_dict(data_tuple):
    field_names = ['id', 'username', 'password', 'role', 'first_name', 'last_name', 'email']
    data_dict = {field: value for field, value in zip(field_names, data_tuple)}
    return data_dict
    

class DatabaseManager:
    def __init__(self,type,**kwargs):
        self.type = type
        self.db = self.connect(**kwargs)

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


class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def email_exists(self, email):
        cursor = self.db_manager.db_connection.cursor()

        query = "SELECT * FROM credentials WHERE email = %s"
        cursor.execute(query, (email,))

        user = cursor.fetchone()

        cursor.close()

        return user is not None

    def username_exists(self, username):
        cursor = self.db_manager.db_connection.cursor()
        query = "SELECT * FROM credentials WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        return user is not None

    def login(self, username, password):
        cursor = self.db_manager.db_connection.cursor()

        #to check login
        query = "SELECT * FROM credentials WHERE BINARY username = %s AND BINARY password = %s"
        cursor.execute(query, (username, password))

        user = cursor.fetchone()

        cursor.close()

        if user:
            QMessageBox.information(None, 'Login Successful', f'Welcome, {username}')
            return True
        else:
            QMessageBox.warning(None, 'Login Failed', 'Invalid username, password.')
            return False





