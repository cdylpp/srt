from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout
from login_window import Ui_Form
from database import DatabaseManager
from user import User, UserManager
from utils import Validator

class LoginWindow(QtWidgets.QDialog):

    login_accepted = pyqtSignal(UserManager)
    login_reject = pyqtSignal()
    login_window_closed = pyqtSignal()
    
    def __init__(self, db_type, **kwargs) -> None:
        super().__init__()
        self.db_manager = DatabaseManager(db_type, **kwargs)
        self.user_manager = UserManager()
        self.app_data = kwargs['app_data']
        
        self.init_ui()

    def init_ui(self):
        # logging info
        print("Init Login View")
        self.setWindowTitle("SRT Login")
        icon = QIcon("srtv3\images\StaySmartLogo1")  # Specify the path to your icon file
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

        # show the ui_form
        self.show()

    def on_login_clicked(self):
        username,password = self.get_user_info()
        if self.valid_login(username, password):
            # Successful Login
            # Set the user in user manager
            self.accept()
            self.user_manager.set_user(self.db_manager.get_user(username, password)) 
            user = self.user_manager.get_user()

            msg_box = QtWidgets.QMessageBox()
            icon = QIcon("srtv3\images\StaySmartLogo1")
            self.setWindowIcon(icon)
            msg_box.setWindowTitle('Login Successful')
            msg_box.setText(f'Welcome, {user.get_name()}!')

            # Apply styles to the QMessageBox
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: rgb(52, 53, 65);
                }
                QLabel {
                    color: white;
                }
                QPushButton {
                    color: white;
                    background-color: black;
                    border: 1px solid black;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: gray;
                }
            """)

            # Create a layout for the message box
            layout = QVBoxLayout()
            layout.addWidget(msg_box)
            msg_box.setLayout(layout)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            msg_box.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)  # Allow text selection
            msg_box.exec()

            self.handle_remember_me(self.ui.remembeme_checkBox.isChecked())
            
            # Signal User Manager to the MainWindow
            self.login_accepted.emit(self.user_manager)
            self.close()

        else:
            # Unsuccessful
            self.on_rejection()
    
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
        if self.ui.password_input.echoMode() == QtWidgets.QLineEdit.EchoMode.Normal:
            self.ui.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        else:
            self.ui.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)

    def show_forgot_pass_window(self):
        forgot_pass_window = ForgotPassWindow(self.db_manager)
        forgot_pass_window.exec()
    
class ForgotPassWindow(QtWidgets.QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle('Reset Password')
        icon = QIcon("srtv3\images\StaySmartLogo1")  # Specify the path to your icon file
        self.setWindowIcon(icon)

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
        

        
