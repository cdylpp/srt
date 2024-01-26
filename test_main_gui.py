from home_view import MainWindow
import sys
from PyQt6.QtWidgets import QApplication

print("Starting application...")
app = QApplication([])

home = MainWindow()
home.show()

sys.exit(app.exec())