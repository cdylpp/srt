import csv
from sqlalchemy import create_engine, text
from PyQt6.QtWidgets import QMessageBox


def csv_to_dict(file_path):
    """Takes a file_path and returns a list of dicts whose key is `username`"""
    rows = []
    with open(file_path, 'r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            rows.append(dict(row))
    return rows

    

class DatabaseManager:
    def __init__(self,type,**kwargs):
        self.type = type
        self.db_engine = self.connect(**kwargs)
    
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
            **db_url (str): database url 

        Returns:
            PooledMySQLConnection | MySQLAbstractConnection: see `mysql.connector.connect`
            List[dict[str, str]]: List of dicts with fields as keys and attributes as values.
        """
        if self.type == "mysql":
            return create_engine(kwargs['db_url'], echo=True)
        
        if self.type == "csv":
            return csv_to_dict(kwargs['file'])

    def close_connection(self):
        if self.type == 'mysql':
            if self.db_connection.is_connected():
                self.db_connection.close()
    
    def is_valid(self, username, password):
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
        
            try:
                with self.db_engine.connect() as conn:
                    result = conn.execute(
                        text("SELECT * FROM admin_credentials WHERE username =:username AND password =:password"),
                        {'username': username, 'password': password}
                    )

                    if result.fetchone():
                        return True
                    else:
                        # Failed Login
                        return False

            except Exception as e:
                print(f"Error: {e}")

    
    def get_user(self,username):
        """returns credientials for `username`"""

        # returns the entire dict for username in csv file
        if self.type == "csv":
            for user in self.db:
                if user['username'] == username:
                    return user
            raise KeyError(f"{username} not in {self.file_name}")

        # returns row with username == `username` as a dict object
        elif self.type == "mysql":
            with self.db_engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM admin_credentials WHERE username =:username"),
                    {'username': username}
                    )
                return result.mappings().first()





