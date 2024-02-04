# Version 2.3
# The Main Application
# 
#
#

import sys, os
from PySide6.QtWidgets import QApplication
from ui.MainWindow import MainWindow
from ui.LoginWindow import LoginWindow
from tests.user import UserManager
from dotenv import load_dotenv

load_dotenv()

class SrtApp(QApplication):
    def __init__(self):
        super().__init__()

        self.show_login()
        self.main_window = None

    def show_login(self):
        login = LoginWindow('mysql', db_url=os.getenv("DB_URL"))
        login.login_reject.connect(self.show_login)  # Connect rejection to show login again
        login.login_accepted.connect(self.on_login_accepted)
        login.exec()

    def on_login_accepted(self, user_manager):
        # Pass User Manager to the MainWindow
        self.main_window = MainWindow(user_manager)
        self.main_window.show()

if __name__ == "__main__":
    srtApp = SrtApp()
    sys.exit(srtApp.exec())

