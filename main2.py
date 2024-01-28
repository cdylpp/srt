# Version 2.0
# Top Level Main Application File
# Runs QApplication in event-loop.
# Shows QMainWindow MySrtApp()
# 
#
#

import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from srt_app import MainWindow
from login_view import LoginDialog

class SrtApp(QApplication):
    def __init__(self):
        super().__init__()
        # Login
        self.login_action()

        self.main_window = MainWindow()
        self.main_window.show()


    # Handles Login Action
    def login_action(self):
        """
        Handles the login_view for user authentication.

        Returns:
            A User is returned.
        """
        # Generate Login Window
        login = LoginDialog('mysql', db_url=os.getenv("DB_URL"))
        # Run Login Loop
        login.exec()
        login.login_reject.connect(login.exec)
        # Exit: Fail / Success
        # Get User from UserManager, send to the MainWindow.
        if not login.accept:
            sys.exit()
            
        return 
        

srtApp = SrtApp()


srtApp.exec()

