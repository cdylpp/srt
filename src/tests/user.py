# User Class
# TODO: Finish User Model
import json
import os



class User:
    def __init__(self, info: dict[str, str]):
        self._info = info
        self._id = info['id']
        self._username = info['username']
        self._email = info['email']
        self._first_name = info['first_name']
        self._last_name = info['last_name']
        self._role = info['role']
    
    def __repr__(self) -> str:
        return f'User(id: {self._id}, username: {self._username})'
    
    def get_username(self) -> str:
        return self._username
    
    def get_email(self) -> str:
        return self._email
    
    def get_name(self) -> str:
        return f'{self._first_name} {self._last_name}'
    
    def get_role(self):
        return self._role
    
    def get_user_data(self):
        return self._info
    
    

class UserManager:
    def __init__(self):
        self._user = None
        self._login_attempts = 0

    def set_user(self, user_data: dict[str, str]) -> None:
        self._user = User(user_data)

    def __repr__(self) -> str:
        return f"UserManager(user: {self._user})"
    
    def get_user(self) -> User:
        return self._user

    def failed_attempt(self) -> None:
        self._login_attempts += 1
        return
    
    def get_login_attempts(self) -> int:
        return self._login_attempts
    
    def clear_user(self) -> None:
        self._profile_data['prev_user'] = ""
        self.update_json()
        return

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

    def handle_login_attempts(self, username) -> None:
        return
        
    def reset_login_attempts(self, username):
        cursor = self.db_manager.db_connection.cursor()

        # Reset login attempts and lockout status on successful login
        query = "UPDATE admin SET login_attempts = 0, locked_out_until = NULL WHERE username = %s"
        cursor.execute(query, (username,))

        cursor.close()
        return
