import csv
from sqlalchemy import create_engine, text
from PyQt6.QtWidgets import QMessageBox

# Config for AWS database, don't change
DB_CONFIG = {
    'host': "srt-database-1.cve60ywu8ysv.us-west-1.rds.amazonaws.com",
    'user': 'srtAdmin',
    'password': 'Bubmi1-xynvez-kijpuv',
    'database': 'srtdatabase'
}

DB_URL = 'mysql://srtAdmin:Bubmi1-xynvez-kijpuv@srt-database-1.cve60ywu8ysv.us-west-1.rds.amazonaws.com/srtdatabase'


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
    
    def get_email(self,email: str) -> dict[str, str]:
        if self.type == 'csv':
            # handle csv case
            return
        
        elif self.type == 'mysql':
            # handle mysql case
            with self.db_engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM admin_credentials WHERE email =:email"),
                    {'email': email}
                    )   
            return result.one_or_none()

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
            with self.db_engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM admin_credentials WHERE username =:username AND password =:password"),
                    {'username': username, 'password': password}
                )

                return True if result else False
    
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





