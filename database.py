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
            query = "SELECT * FROM admin_credentials WHERE email = %s"
            cursor.execute(query, (target,))
            result = cursor.fetchone()
            cursor.close
            return generate_credential_dict(result)

    
    def connect(self, **kwargs):
        """
        Makes a connection to the database.
        
        Args:
            **file (str): path to csv file to connect too (for type=`csv`)
            **host (str): host url for database to connect to.
            **user (str): username for the database.
            **password (str): password for the `mysql` database.
            **database (str): name of the database for `mysql` database.

        Returns:
            PooledMySQLConnection | MySQLAbstractConnection: see `mysql.connector.connect`
            List[dict[str, str]]: List of dicts with fields as keys and attributes as values.
        """
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


# James' Push
class UserManager:
    def init(self, db_manager):
        self.db_manager = db_manager

    def email_exists(self, email):
        cursor = self.db_manager.db_connection.cursor()

        query = "SELECT * FROM admin WHERE email = %s"
        cursor.execute(query, (email,))

        user = cursor.fetchone()

        cursor.close()

        return user is not None

    def username_exists(self, username):
        cursor = self.db_manager.db_connection.cursor()
        query = "SELECT * FROM admin WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        return user is not None
    
    def login(self, username, password):
        cursor = self.db_manager.db_connection.cursor()

        # Execute SELECT query to check login admin
        query = "SELECT * FROM admin WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        user = cursor.fetchone()

        if user:
            # Reset login attempts on successful login
            self.reset_login_attempts(username)
            QMessageBox.information(None, 'Login Successful', f'Welcome, {username}')
            return True
        else:
            # Increment login attempts and set indefinite lockout
            self.handle_login_attempts(username)
            return False

    def handle_login_attempts(self, username):
        cursor = self.db_manager.db_connection.cursor()

        # Retrieve current login attempts count and lockout status
        query = "SELECT login_attempts, locked_out_until FROM admin_credentials WHERE username = %s"
        cursor.execute(query, (username,))
        user_info = cursor.fetchone()

        if user_info:
            login_attempts, locked_out_until = user_info

            # Increment login attempts
            login_attempts += 1

            # Set indefinite lockout
            locked_out_until = datetime.max

            # Update login attempts and lockout status in the database
            update_query = "UPDATE admin_credentials SET login_attempts = %s, locked_out_until = %s WHERE username = %s"
            cursor.execute(update_query, (login_attempts, locked_out_until, username))

            # Display lockout message
            QMessageBox.warning(None, 'Account Locked', 'Too many unsuccessful login attempts.')

        cursor.close()
        
    def reset_login_attempts(self, username):
        cursor = self.db_manager.db_connection.cursor()

        # Reset login attempts and lockout status on successful login
        query = "UPDATE admin SET login_attempts = 0, locked_out_until = NULL WHERE username = %s"
        cursor.execute(query, (username,))

        cursor.close()

