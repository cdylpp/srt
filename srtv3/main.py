import sys, os, subprocess
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSlot
from AppDataManager import AppDataManager
from LoginWindow import LoginWindow
from views import MainWindow
from dotenv import load_dotenv
import pyqtgraph as pg
import qdarktheme
from user import UserManager
from paths import Paths

DB_URL = "mysql://srtAdmin:Bubmi1-xynvez-kijpuv@srt-database-1.cve60ywu8ysv.us-west-1.rds.amazonaws.com/srtdatabase"
AUTH_FLAG = False

try:
    from ctypes import windll
    appid = "nu.capstone.srt.v3"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
except ImportError:
    pass

load_dotenv()


def load_app_data():
    print("Loading app data")
    return AppDataManager()

def on_login_accepted():
    global AUTH_FLAG
    AUTH_FLAG = True

def on_sign_out(app):
    app.quit()
    sys.exit()


@pyqtSlot()
def cleanup_before_quit(s):
    if not s:
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

    srtApp = QApplication(sys.argv)
    qdarktheme.setup_theme()
    app_data = load_app_data()

    login = LoginWindow('mysql', db_url=DB_URL, app_data=app_data)
    login.user_manager = UserManager(app_data)
    login.login_accepted.connect(on_login_accepted)
    login.login_window_closed.connect(cleanup_before_quit)
    login.rejected.connect(lambda: cleanup_before_quit(False))  #to close loginwindow upon clicking exit

    while not AUTH_FLAG:
        login.exec()
    
    main_window = MainWindow(login.user_manager, app_data_manager=app_data) #added '_manager' to app_data
    main_window.browser_closed.connect(on_close_main)
    main_window.sign_out.connect(lambda: on_sign_out(srtApp))  # Handle the sign-out signal
    main_window.show()  # Show the main window

    srtApp.setWindowIcon(QIcon(Paths.image("StaySmartLogo1.png")))
    sys.exit(srtApp.exec())





