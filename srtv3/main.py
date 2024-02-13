import sys, os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSlot
from AppDataManager import AppDataManager
from LoginWindow import LoginWindow
from views import MainWindow
from dotenv import load_dotenv
import pyqtgraph as pg

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
    srtApp = QApplication([])
    app_data = load_app_data()
    show_login()

    sys.exit(srtApp.exec())





