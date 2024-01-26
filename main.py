import sys
from PyQt6.QtWidgets import QApplication
from login_view import LoginWindow
from home_view import MainWindow
from dotenv import load_dotenv
import os
load_dotenv()

print("Starting application...")
app = QApplication([])

# Use for `mysql` database
# AWS RDS Mysql
# show login, the login window is the view.
login = LoginWindow('mysql', db_url=os.getenv("DB_URL"))

home = MainWindow()

login.login_success.connect(home.show)

login.show()

# Use for `csv` database
# login = LoginWindow('csv', file='Credentials.csv')

sys.exit(app.exec())