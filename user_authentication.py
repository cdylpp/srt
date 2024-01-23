from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDialog
from database import DatabaseManager, UserManager

class UserManagementApp(QWidget):
    def __init__(self):
        super().__init__()

        self.db_manager = DatabaseManager("localhost", "root", "NU2024", "user_management")
        self.user_manager = UserManager(self.db_manager)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('SRT Login')

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton('Login')
        self.forgot_button = QPushButton('Forgot Password')

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

        if self.user_manager.login(username, password):
            QMessageBox.information(self, 'Login Successful', f'Welcome, {username}')
            self.close()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username, password.')

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

        if '@' in email:
            cursor = self.db_manager.db_connection.cursor()
            query = "SELECT email FROM credentials WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                QMessageBox.information(None, 'Password Reset', 'Email sent!')
            else:
                QMessageBox.warning(self, 'Password Reset Failed', 'Email not found. Please contact your admin.')
        else:
            QMessageBox.warning(self, 'Invalid Email', 'Please enter a valid email address.')

if __name__ == '__main__':
    app = QApplication([])
    user_management_app = UserManagementApp()
    app.exec()

