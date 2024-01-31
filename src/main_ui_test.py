# Runs the Main UI Window without the login.
# 
#


import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from ui.MainWindow import MainWindow
from ui.login_view import LoginDialog
from dotenv import load_dotenv

load_dotenv()

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

app = QApplication()
window = MainWindow()
window.show()
app.exec()