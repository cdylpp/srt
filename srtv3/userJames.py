# User Class
# TODO: Finish User Model
import sys, os, json
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QFont, QPixmap

import AppDataManager


class ProfileDialog(QWidget):
    def __init__(self, user):
        super().__init__()
        self._user = user
        self.initializeUI()

    def initializeUI(self):
        """Set up the application's GUI."""
        self.setFixedSize(250, 400)
        self.setWindowTitle(f"{self._user.get_name()}")

        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        """Create the labels to be displayed in the window."""
        self.createImageLabels()

        user_label = QLabel(self)
        user_label.setText(f"{self._user.get_name()}")
        user_label.setFont(QFont("Arial", 20))
        user_label.move(85, 140)

        permissions_label = QLabel(self)
        permissions_label.setText("Permissions")
        permissions_label.setFont(QFont("Arial", 15))
        permissions_label.move(15, 170)

        role_info = QLabel(self)
        role_info.setText(f"{self._user.get_role()}")
        role_info.setWordWrap(True)
        role_info.move(15, 190)

        acct_label = QLabel(self)
        acct_label.setText("Account Info")
        acct_label.setFont(QFont('Arial', 17))
        acct_label.move(15, 240)

        acct_info = QLabel(self)
        acct_info.setText(f"username: {self._user.get_username()}\nemail: {self._user.get_email()}")
        acct_info.move(15, 260)



    def createImageLabels(self):
        """Open image files and create image labels."""
        images = ["images/skyblue.png", 
                  "images/profile_image.png"]

        for image in images:
            try:
                with open(image):
                    label = QLabel(self)
                    pixmap = QPixmap(image)
                    label.setPixmap(pixmap)
                    if image == "images/profile_image.png":
                        label.move(80, 20) 
            except FileNotFoundError as error:
                print(f"Image not found.\nError: {error}")            


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
    def __init__(self, app_data_manager: AppDataManager):
        self.max_attempts = 3
        self._user = None
        self.app_data_manager = app_data_manager

    def is_locked_out(self, username) -> bool:
        return self.app_data_manager.is_user_locked_out(username)

    def handle_login_attempts(self, username, success: bool) -> None:
        if success:
            self.app_data_manager.set_login_attempts(username, 0)
            self.app_data_manager.set_user_lockout(username, False)
        else:
            attempts = self.app_data_manager.get_login_attempts(username) +1
            self.app_data_manager.set_login_attempts(username, attempts)
            if attempts >= self.max_attempts:
                self.app_data_manager.set_user_lockout(username, True)

    def set_user(self, user_data: dict[str, str]) -> None:
        self._user = User(user_data)

    def __repr__(self) -> str:
        return f"UserManager(user: {self._user})"
    
    def get_user(self) -> User:
        return self._user
    
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


