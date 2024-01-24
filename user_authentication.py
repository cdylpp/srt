from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDialog
from database import DatabaseManager, UserManager, CSVManager
#from home_screen import HomeScreen

class UserManagementApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager("localhost", "root", "009243286", "user_management")
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

    def show_login_window(self, user_type):
        print(f"Clicked {user_type} button...")
        login_window = StudentLoginWindow(self.db_manager) if user_type == 'Student' else LoginWindow(self.db_manager, user_type)

        result = login_window.exec()

        print("Dialog Result:", result)

        if result == QDialog.DialogCode.Accepted:
            username = login_window.username_input.text()
            cursor = self.db_manager.db_connection.cursor()

            if user_type == 'Student':
                query = f"SELECT first_name, last_name FROM credentials WHERE id = %s"
            else:
                query = f"SELECT first_name, last_name FROM credentials WHERE username = %s AND role = %s"

            cursor.execute(query, (username,)) if user_type == 'Student' else cursor.execute(query, (username, user_type))
            result = cursor.fetchone()
            cursor.close()

            if result:
                full_name = f"{result[0]} {result[1]}"
            else:
                full_name = f"Unknown {user_type}"

            QMessageBox.information(None, 'Login Successful', f'Welcome {user_type} {full_name}!')

            #self.show_home_screen(user_type, full_name)

    # def show_home_screen(self, user_type, full_name):
    #     home_screen = HomeScreen(user_type, full_name, self.db_manager)
    #     home_screen.show()

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
    print("Starting application...")
    app = QApplication([])
    login = LoginWindow('Credentials.csv', 'Admin')
    app.exec()


