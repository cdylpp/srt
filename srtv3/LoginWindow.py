from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from login_window import Ui_Form
from database import DatabaseManager
from user import UserManager
from paths import Paths
from utils import Validator
class LoginWindow(QtWidgets.QDialog):

    login_accepted = pyqtSignal(UserManager)
    login_reject = pyqtSignal()
    login_window_closed = pyqtSignal()
    
    def __init__(self, db_type, **kwargs) -> None:
        super().__init__()
        self.db_manager = DatabaseManager(db_type, **kwargs)
        self.user_manager = UserManager(kwargs['app_data'])
        self.app_data = kwargs['app_data']
        
        self.init_ui()

    def init_ui(self):
        # logging info
        print("Init Login View")
        self.setWindowTitle("StaySmart: Student Retention Tool")
        icon = QIcon(Paths.image("StaySmartLogo1.png")) # Specify the path to your icon file
        self.setWindowIcon(icon)

        # Wrap ui in Form widget
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.lineEdit.setText(self.app_data.get_prev_user())
        
        # connect buttons
        self.ui.login_button.clicked.connect(self.on_login_clicked)
        self.ui.forgot_button.clicked.connect(self.show_forgot_pass_window)
        self.ui.visibility_button.clicked.connect(self.show_hide_password) #visibility button .widget
        self.ui.remembeme_checkBox.clicked.connect(self.on_remember_me) #rememberme button
        # Connect username field text change to re-enable password field
        self.ui.lineEdit.textChanged.connect(self.on_username_changed)

        # show the ui_form
        self.show()

    def on_username_changed(self):
        # Re-enable the password field whenever the username is changed
        self.ui.password_input.setDisabled(False)

    def on_login_clicked(self):
        username,password = self.get_user_info()
        if self.user_manager.is_locked_out(username):
            QtWidgets.QMessageBox.warning(self, 'Account Locked', 'Your account is locked. Please contact your system '
                                                                  'administrator')
            self.ui.password_input.setDisabled(True) # Disable the password field
            return

        if self.valid_login(username, password):
            # Successful Login
            # Set the user in user manager
            self.accept()
            self.user_manager.set_user(self.db_manager.get_user(username, password)) 
            user = self.user_manager.get_user()
            # Reset login attempts on successful login
            self.user_manager.handle_login_attempts(username, success=True)

            msg_box = QtWidgets.QMessageBox()
            msg_box.setStyleSheet("QLabel { color: white; }")
            msg_box.information(self, 'Login Successful', f'Welcome, {user.get_name()}!')


            self.handle_remember_me(self.ui.remembeme_checkBox.isChecked())
            
            # Signal User Manager to the MainWindow
            self.login_accepted.emit(self.user_manager)
            self.close()

        else:
            # Handle failed login attempt
            self.user_manager.handle_login_attempts(username, success=False)
            QtWidgets.QMessageBox.warning(self, 'Login Failed', 'Invalid credentials.')
            # Check if user should be locked out
            if self.user_manager.is_locked_out(username):
                self.ui.password_input.setDisabled(True)
            self.login_reject.emit()
    
    def get_user_info(self):
        """
        get user info from the database
        """
        username = self.ui.lineEdit.text()
        password = self.ui.password_input.text()
        return username, password
    
    def valid_login(self, usr, pwd):
        return self.db_manager.is_valid(usr, pwd)
    
    def on_rejection(self):
        self.reject()
        QtWidgets.QMessageBox.warning(self, 'Login Failed', 'Invalid credentials.')
        self.user_manager.failed_attempt()
        if self.user_manager.get_login_attempts() > 2:
            # Youre done! No more!
            raise PermissionError("Failed Attempt Three Times, Locked From Account.")

        self.login_reject.emit()

    # Remember me function
    def on_remember_me(self):
        if self.ui.remembeme_checkBox.isChecked():
            self.ui.remembeme_checkBox.setText("Login info saved!")
        else:
            self.ui.remembeme_checkBox.setText("Remember Me")

    def handle_remember_me(self, login_successful):
        if login_successful:
            self.app_data.save_user(self.user_manager.get_user().get_username())
        else:
            self.app_data.clear_prev_user()
        return

    def show_hide_password(self):
        if self.ui.password_input.echoMode() == QtWidgets.QLineEdit.Normal:
            self.ui.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        else:
            self.ui.password_input.setEchoMode(QtWidgets.QLineEdit.Normal)

    def show_forgot_pass_window(self):
        forgot_pass_window = ForgotPassWindow(self.db_manager)
        forgot_pass_window.exec()
    
class ForgotPassWindow(QtWidgets.QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle('Forgot Password?')
        icon = QIcon(Paths.image("StaySmartLogo1.png"))  # Specify the path to your icon file
        self.setWindowIcon(icon)

        self.email_label = QtWidgets.QLabel('Email:')
        self.email_input = QtWidgets.QLineEdit()
        self.reset_button = QtWidgets.QPushButton('Reset Password')
        self.cancel_button = QtWidgets.QPushButton('Cancel')

        # Set stylesheets
        self.setStyleSheet("background-color: #343541;")
        self.email_input.setStyleSheet("border: none; background-color: #FFFFFF; color: black;")
        self.reset_button.setStyleSheet("background-color: #00A8E9; color: #FFFFFF;")
        self.cancel_button.setStyleSheet("background-color: black; color: #FFFFFF;")

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
        

        

