import sys
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDialog, QCheckBox
from PySide6.QtCore import Signal
from database import DatabaseManager
from tests.user import User, UserManager
from utils import Validator
from dotenv import dotenv_values

class LoginDialog(QDialog):

    login_accept = Signal(bool)
    login_reject = Signal(bool)

    def __init__(self, db_type, **kwargs):
        super().__init__()
        self.db_manager = DatabaseManager(db_type, **kwargs)
        self.user_manager = UserManager()
        self.init_ui()
        self.accept = False

    def init_ui(self):
        print("Init Login View")
        self.setWindowTitle('SRT Login')

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit(self.user_manager.get_prev_user())

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.rememberme_checkBox = QCheckBox('Remember Me')

        self.login_button = QPushButton('Login')
        self.forgot_button = QPushButton('Forgot Password')

        self.resize(300, 350)
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.rememberme_checkBox)
        layout.addWidget(self.login_button)
        layout.addWidget(self.forgot_button)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.login)
        self.forgot_button.clicked.connect(self.show_forgot_pass_window)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.db_manager.is_valid(username, password):
            # Successful Login
            self.user_manager.set_user(self.db_manager.get_user(username))
            user = self.user_manager.get_user()
            QMessageBox.information(self, 'Login Successful', f'Welcome, {user.get_name()}!')

            if self.rememberme_checkBox.isChecked():
                self.user_manager.save_user()
                self.rememberme_checkBox.setText("Login info saved!")
            else:
                self.user_manager.clear_user()
            
            # Signal login successful
            self.login_accept.emit(True)
            self.accept = True
            self.close()

        else:
            # Unsuccessful
            QMessageBox.warning(self, 'Login Failed', 'Invalid credentials.')

            self.user_manager.failed_attempt()
            if self.user_manager.get_login_attempts() > 2:
                # Youre done! No more!
                raise PermissionError("Failed Attempt Three Times, Locked From Account.")

            self.login_reject.emit(True)
            return False


    def show_forgot_pass_window(self):
        forgot_pass_window = ForgotPassWindow(self.db_manager)
        forgot_pass_window.exec()

    def set_user_text(self):
        env_vals = dotenv_values('.env')
        saved_user = env_vals.get('PREV_USER')
        return str(saved_user)



class ForgotPassWindow(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle('Reset Password')

        self.email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        self.reset_button = QPushButton('Reset Password')
        self.cancel_button = QPushButton('Cancel')

        layout = QVBoxLayout()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

        self.reset_button.clicked.connect(self.reset_password)
        self.cancel_button.clicked.connect(self.close)

    def reset_password(self):
        email = self.email_input.text()

        if Validator().validate('email', email):
            if self.db_manager.get_email(email):
                QMessageBox.information(None, 'Password Reset', 'Email sent!')
                # implement send email logic
            else:
                QMessageBox.warning(self, 'Password Reset Failed', 'Email not found. Please contact your admin.')
        else:
            QMessageBox.warning(self, 'Invalid Email', 'Please enter a valid email address.')
            self.email_input.clear()