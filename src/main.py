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
from tests.AppDataManager import AppDataManager
from dotenv import load_dotenv

load_dotenv()

class SrtApp(QApplication):
    def __init__(self):
        super().__init__()
        self._app_data = self.load_app_data()
        self.main_window = None
        self.aboutToQuit.connect(self.cleanup_before_quit)
        self.show_login()

    def show_login(self):
        login = LoginWindow('mysql', db_url=os.getenv("DB_URL"), app_data=self._app_data)
        login.login_reject.connect(self.show_login)  # Connect rejection to show login again
        login.login_accepted.connect(self.on_login_accepted)
        login.login_window_closed.connect(self.cleanup_before_quit)
        login.exec()

    def on_login_accepted(self, user_manager):
        # Pass User Manager to the MainWindow
        self.main_window = MainWindow(user_manager, app_data=self._app_data)
        self.main_window.main_window_closed.connect(self.on_close_main)
        self.main_window.show()

    def cleanup_before_quit(self):
        print("Quit Clean up.")
        self.quit()
    
    def load_app_data(self):
        print("Loading app data")
        return AppDataManager()
    
    def on_close_main(self):
        self.cleanup_before_quit()
        sys.exit()



if __name__ == "__main__":
    srtApp = SrtApp()
    sys.exit(srtApp.exec())

