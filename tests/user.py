# User Class
# TODO: Finish User Model
import shelve

class User:
    def __init__(self, info: dict[str, str]):
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

    def save_user(self) -> None:
        # Save the username if the check box is checked.
        with shelve.open('profile') as profile:
            profile['prev_user'] = self._user.get_username()
        return
    
    def clear_user(self) -> None:
        with shelve.open('profile') as profile:
            profile['prev_user'] = ""
        return
    
    def get_prev_user(self) -> str:
        with shelve.open('profile') as profile:
            if 'prev_user' in profile:
                return profile['prev_user']
            else:
                return ""

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
    
    def login(self, username, password) -> None:
            return False

    def handle_login_attempts(self, username) -> None:
        return
        
    def reset_login_attempts(self, username):
        cursor = self.db_manager.db_connection.cursor()

        # Reset login attempts and lockout status on successful login
        query = "UPDATE admin SET login_attempts = 0, locked_out_until = NULL WHERE username = %s"
        cursor.execute(query, (username,))

        cursor.close()