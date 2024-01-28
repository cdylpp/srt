from PySide6.QtCore import Slot
from main_view import Ui_MainWindow, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setWindowTitle("Smart Solutions")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect Buttons
        self.connect_button(self.ui.helpBtn, "help button pressed")
        self.connect_button(self.ui.menuBtn, "menu button pressed")
        self.connect_button(self.ui.homeBtn, "home button pressed")
        self.connect_button(self.ui.dataBtn, "data button pressed")
        self.connect_button(self.ui.reportBtn, "report button pressed")
        self.connect_button(self.ui.settingsBtn, "settings button pressed")
        self.connect_button(self.ui.infoBtn, "info button pressed")
        self.connect_button(self.ui.minimizeBtn, "minimize button pressed")
        self.connect_button(self.ui.restoreBtn, "restore button pressed")
        self.connect_button(self.ui.closeBtn, "close button pressed")
        self.connect_button(self.ui.pushButton, "push button pressed")
        self.connect_button(self.ui.profileBtn, "profile button pressed")
        self.connect_button(self.ui.pushButton_6, "pushbutton 6 button pressed")
        self.connect_button(self.ui.pushButton_7, "pushbutton 7 pressed")
        self.connect_button(self.ui.pushButton_8, "pushbutton 8 pressed")

    def connect_button(self, button, msg):
        button.clicked.connect(lambda: self.button_pressed(msg))

    @Slot()
    def button_pressed(self, msg):
        print(msg)
        
    
        
    
    


