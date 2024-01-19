import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def close_connection(self):
        if self.db_connection.is_connected():
            self.db_connection.close()

class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def email_exists(self, email, user_type):
        cursor = self.db_manager.db_connection.cursor()

        query = f"SELECT * FROM credentials WHERE email = %s AND role = %s"
        cursor.execute(query, (email, user_type))

        user = cursor.fetchone()

        cursor.close()

        return user is not None

    def username_exists(self, username, user_type):
        cursor = self.db_manager.db_connection.cursor()
        query = f"SELECT * FROM credentials WHERE username = %s AND role = %s"
        cursor.execute(query, (username, user_type))
        user = cursor.fetchone()
        cursor.close()
        return user is not None

    def login(self, username, password, user_type):
        cursor = self.db_manager.db_connection.cursor()

        if user_type == 'Student':
            query = f"SELECT * FROM credentials WHERE id = %s AND password = %s AND role = %s"
        else:
            query = f"SELECT * FROM credentials WHERE username = %s AND password = %s AND role = %s"

        cursor.execute(query, (username, password, user_type))

        user = cursor.fetchone()

        cursor.close()

        if user:
            return True
        else:
            return False


