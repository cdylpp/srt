import sys
from PyQt6.QtWidgets import QApplication
from login_view import LoginWindow
from database import DB_URL

print("Starting application...")
app = QApplication([])

# Use for `mysql` database
# AWS RDS Mysql
login = LoginWindow('mysql', db_url=DB_URL)

# Use for `csv` database
# login = LoginWindow('csv', file='Credentials.csv')

sys.exit(app.exec())