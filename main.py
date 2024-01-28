# Version 1.0
# Top Level Main Application File
# Runs QApplication in event-loop.
# Shows QMainWindow MainWindow()
#
#
#

import sys
from PyQt6.QtCore import Slot
from PyQt6.QtWidgets import QApplication
from login_view import LoginDialog
from home_view import MainWindow
from srt_app import MySrtApp
from dotenv import load_dotenv
import os
load_dotenv()


class SrtApp(QApplication):
    def __init__(self):
        super().__init__()

        self.login = LoginDialog('mysql', db_url=os.getenv("DB_URL"))
        self.home_window = MySrtApp()
        self.user = None

        login.user_signal.connect(self.get_user)
        login.login_signal.connect(self.home_window.show)

    @Slot()
    def get_user(self):
        self.user = self.login.get_user()
        return



print("Starting application...")
srtApp = QApplication([])

# Use for `mysql` database
# AWS RDS Mysql
# show login, the login window is the view.
login = LoginDialog('mysql', db_url=os.getenv("DB_URL"))

home = MainWindow()

login.login_signal.connect(home.show)

login.show()

# Use for `csv` database
# login = LoginWindow('csv', file='Credentials.csv')

sys.exit(app.exec())