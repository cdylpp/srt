import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDialog
from database import DatabaseManager, DB_CONFIG
from utils import Validator

class LoginWindow(QWidget):
    def __init__(self, db_type, **kwargs):
        super().__init__()
        self.db_manager = DatabaseManager(db_type,**kwargs)
        self.init_ui()

    def init_ui(self):
        print("Initializing UI...")
        self.setWindowTitle('SRT Login')

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton('Login')
        self.forgot_button = QPushButton('Forgot Password')

        self.resize(300, 350)
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.forgot_button)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.login)
        self.forgot_button.clicked.connect(self.show_forgot_pass_window)
        

        self.show()

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.db_manager.login(username, password):
            credentials = self.db_manager.getCredentials(username)
            QMessageBox.information(self, 'Login Successful', f'Welcome, {credentials["first_name"]}!')
            self.close()
            return True
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username, password.')
            return False

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
            result = self.db_manager.fetch(field='email', target=email)
            if result:
                QMessageBox.information(None, 'Password Reset', 'Email sent!')
            else:
                QMessageBox.warning(self, 'Password Reset Failed', 'Email not found. Please contact your admin.')
        else:
            QMessageBox.warning(self, 'Invalid Email', 'Please enter a valid email address.')
            self.email_input.clear()

if __name__ == '__main__':


    print("Starting application...")
    app = QApplication(sys.argv)
    
    # Use for `mysql` database
    # AWS RDS Mysql
    login = LoginWindow('mysql',
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )
    
    
    # Use for `csv` database
    # login = LoginWindow('csv', file='Credentials.csv')
    
    
    sys.exit(app.exec())


