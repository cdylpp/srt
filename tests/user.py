# User Class
# TODO: Finish User Model
class User:
    def __init__(self, info: dict[str, str]):
        self.__id = info['id']
        self.__username = info['username']
        self.__email = info['email']
        self.__first_name = info['first_name']
        self.__last_name = info['last_name']
        self.__role = info['role']
    
    def __repr__(self):
        return f'User(id: {self.__id}, username: {self.__username})'
    
    def get_email(self):
        return self.__email
    
    def get_name(self):
        return f'{self.__first_name} {self.__last_name}'
    
    def get_role(self):
        return self.__role
    
    

class UserManager:
    def __init__(self):
        self.user = None

    def set_user(self, user_data: dict[str, str]):
        self.user = User(user_data)

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