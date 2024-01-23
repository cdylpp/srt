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
        

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        

        self.setLayout(layout)

        self.login_button.clicked.connect(self.login)
        

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

if __name__ == '__main__':
    app = QApplication([])
    user_management_app = UserManagementApp()
    app.exec()

