# Version 2.0
# Top Level Main Application File
# Runs QApplication in event-loop.
# Shows QMainWindow MySrtApp()
# 
#
#

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from srt_app import MySrtApp

app = QApplication(sys.argv)

window = MySrtApp()

window.show()
app.exec()

