import sys, os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSlot
from AppDataManager import AppDataManager
from LoginWindow import LoginWindow
from views import MainWindow
from dotenv import load_dotenv
import pyqtgraph as pg
import qdarktheme
from user import UserManager

load_dotenv()


def load_app_data():
    print("Loading app data")
    return AppDataManager()

APP_DATA = load_app_data()

def show_login():
    login = LoginWindow('mysql', db_url=os.getenv("DB_URL"), app_data=APP_DATA)
    login.login_reject.connect(show_login)  # Connect rejection to show login again
    login.login_accepted.connect(on_login_accepted)
    login.login_window_closed.connect(cleanup_before_quit)
    login.exec()

def on_login_accepted(user_manager):
    # Pass User Manager to the MainWindow
    main_window = MainWindow(user_manager, app_data=APP_DATA)
    main_window.browser_closed.connect(on_close_main)
    main_window.exec()

@pyqtSlot()
def cleanup_before_quit(s):
    if s:
        # Login Accepted. Window closed to get to main view. Don't exit.
        print("Close login window")
    else:
        # login closed without success. Close application
        print("Quit Clean up.")
        sys.exit()
    
def on_close_main():
    cleanup_before_quit(False)
    


if __name__ == "__main__":
    user_data = {
        "id": 3,
        "username": "c.lepp",
        "password": "A123cl",
        "role": "Admin",
        "first_name": "Cody",
        "last_name": "Lepp",
        "email": "cody.lepp@admin.srt",
        "login_attempts": 0
    }

    srtApp = QApplication([])
    app_data = load_app_data()

    # With Login View
    # show_login() 


    # Without Login View
    user_manager = UserManager()
    user_manager.set_user(user_data)
    main = MainWindow(user_manager, app_data=app_data)
    main.show()
    
    sys.exit(srtApp.exec())





