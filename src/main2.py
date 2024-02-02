# Version 2.1
# Using the New LoginWindow that wraps Ui_Form for login 
# Top Level Main Application File
# Runs QApplication in event-loop.
# Shows QMainWindow MySrtApp()
# 
#
#

import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from ui.MainWindow import MainWindow  #from ui.MainWindow import MainWindow
from ui.login_view import LoginDialog #from ui.login_view import LoginDialog
from ui.LoginWindow import LoginWindow
from dotenv import load_dotenv

load_dotenv()

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

class SrtApp(QApplication):
    def __init__(self):
        super(SrtApp,self).__init__()
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
        login = LoginWindow('mysql', db_url=os.getenv("DB_URL"))  # Old one was LoginDialog
        
        # Run Login Loop
        login.exec()
        login.login_reject.connect(login.exec)
        # Exit: Fail / Success
        # Get User from UserManager, send to the MainWindow.
        if not login.accept:
            sys.exit()
            
        return 
        

if __name__ == "__main__":
    srtApp = SrtApp()


    srtApp.exec()

