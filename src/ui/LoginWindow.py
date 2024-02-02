from PySide6 import QtWidgets, QtCore, QtGui
from ui.login_window import Ui_Form
from database import DatabaseManager
from tests.user import User, UserManager
from utils import Validator
from dotenv import dotenv_values

class LoginWindow(QtWidgets.QDialog):
    login_accept = QtCore.Signal(bool)
    login_reject = QtCore.Signal(bool)
    
    def __init__(self, db_type, **kwargs) -> None:
        super().__init__()
        self.db_manager = DatabaseManager(db_type, **kwargs)
        self.user_manager = UserManager()
        self.accept = False
        
        self.init_ui()

    
    def init_ui(self):
        # logging info
        print("Init Login View")
        self.setWindowTitle("SRT Login")
        
        # Wrap ui in Form widget
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # connect buttons
        self.ui.login_button.clicked.connect(self.login)
        self.ui.forgot_button.clicked.connect(self.show_forgot_pass_window)
        
        # show the ui_form
        self.show()
    
    # Handle the user login
    def login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.password_input.text()

        if self.db_manager.is_valid(username, password):
            # Successful Login
            self.user_manager.set_user(self.db_manager.get_user(username))
            user = self.user_manager.get_user()
            QtWidgets.QMessageBox.information(self, 'Login Successful', f'Welcome, {user.get_name()}!')

            if self.ui.remembeme_checkBox.isChecked():
                self.user_manager.save_user()
                self.ui.remembeme_checkBox.setText("Login info saved!")
            else:
                self.user_manager.clear_user()
            
            # Signal login successful
            self.login_accept.emit(True)
            self.accept = True
            self.close()

        else:
            # Unsuccessful
            QtWidgets.QMessageBox.warning(self, 'Login Failed', 'Invalid credentials.')

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
    
class ForgotPassWindow(QtWidgets.QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle('Reset Password')

        self.email_label = QtWidgets.QLabel('Email:')
        self.email_input = QtWidgets.QLineEdit()
        self.reset_button = QtWidgets.QPushButton('Reset Password')
        self.cancel_button = QtWidgets.QPushButton('Cancel')

        layout = QtWidgets.QVBoxLayout()
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
                QtWidgets.QMessageBox.information(None, 'Password Reset', 'Email sent!')
                # implement send email logic
            else:
                QtWidgets.QMessageBox.warning(self, 'Password Reset Failed', 'Email not found. Please contact your admin.')
        else:
            QtWidgets.QMessageBox.warning(self, 'Invalid Email', 'Please enter a valid email address.')
            self.email_input.clear()       
        

        

