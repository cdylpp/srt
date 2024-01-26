from PySide6.QtCore import Slot
from main_view import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.helpBtn.clicked.connect(self.help_btn_pressed)

    @Slot()
    def help_btn_pressed(self):
        print('help button pressed')
    


