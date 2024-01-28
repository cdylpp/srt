import sys
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDialog, QCheckBox
from PyQt6.QtCore import pyqtSignal
from database import DatabaseManager
from tests.user import User
from utils import Validator

class LoginDialog(QDialog):

    login_accept = pyqtSignal(bool)
    login_reject = pyqtSignal(bool)

    def __init__(self, db_type, **kwargs):
        super().__init__()
        self.db_manager = DatabaseManager(db_type, **kwargs)
        self.user_signal = None
        self.init_ui()

    def init_ui(self):
        print("Initializing UI...")
        self.setWindowTitle('SRT Login')

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()

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

        self.rememberme_checkBox.stateChanged.connect(self.checkBoxStatus)
        self.login_button.clicked.connect(self.login)
        self.forgot_button.clicked.connect(self.show_forgot_pass_window)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        rememberme = self.rememberme_checkBox.isChecked()

        if self.db_manager.login(username, password):
            # Successful Login
            user = User(self.db_manager.get_user(username))
            QMessageBox.information(self, 'Login Successful', f'Welcome, {user.get_name()}!')
            self.login_accept.emit(True)
            self.close()

        else:
            # Unsuccessful
            # TODO: Failed Login
            self.login_reject.emit(True)
            QMessageBox.warning(self, 'Login Failed', 'Invalid credentials.')
            self.close()
            return False

        """ remember box logic """
    def checkBoxStatus(self):
        if self.rememberme_checkBox.isChecked():
            self.rememberme_checkBox.setText("Login info saved!")

        else:
            self.rememberme_checkBox.setText("Remember me")


    def show_forgot_pass_window(self):
        forgot_pass_window = ForgotPassWindow(self.db_manager)
        forgot_pass_window.exec()



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




