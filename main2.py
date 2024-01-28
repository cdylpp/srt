from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys
from srt_app import MySrtApp

app = QApplication(sys.argv)

window = MySrtApp()

window.show()
app.exec()

