import sys
from PyQt6.QtWidgets import QApplication
from login_view import LoginWindow
from database import DB_CONFIG

print("Starting application...")
app = QApplication([])

# Use for `mysql` database
# AWS RDS Mysql
login = LoginWindow('mysql',
    host=DB_CONFIG['host'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    database=DB_CONFIG['database']
)

# Use for `csv` database
# login = LoginWindow('csv', file='Credentials.csv')

sys.exit(app.exec())