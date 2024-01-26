from PySide6.QtCore import Slot
from main_view import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect Buttons
        self.ui.helpBtn.clicked.connect(self.helpBtnPressed)
        self.ui.menuBtn.clicked.connect(self.menuBtnPressed)
        self.ui.homeBtn.clicked.connect(self.homeBtnPressed)
        self.ui.dataBtn.clicked.connect(self.dataBtnPressed)
        self.ui.reportBtn.clicked.connect(self.reportBtnPressed)
        self.ui.settingsBtn.clicked.connect(self.settingsBtnPressed)
        self.ui.infoBtn.clicked.connect(self.infoBtnPressed)
        self.ui.minimizeBtn.clicked.connect(self.minimizeBtnPressed)
        self.ui.restoreBtn.clicked.connect(self.restoreBtnPressed)
        self.ui.closeBtn.clicked.connect(self.closeBtnPressed)
        self.ui.pushButton.clicked.connect(self.pushButtonPressed)
        self.ui.profileBtn.clicked.connect(self.profileBtnPressed)
        self.ui.pushButton_6.clicked.connect(self.pushButton_6Pressed)
        self.ui.pushButton_7.clicked.connect(self.pushButton_7Pressed)
        self.ui.pushButton_8.clicked.connect(self.pushButton_8Pressed)
    
    @Slot()
    def pushButton_8Pressed(self):
        print("pushbutton_8 pressed")
    
    @Slot()
    def pushButton_7Pressed(self):
        print("pushbutton_7 pressed")
    
    @Slot()
    def pushButton_6Pressed(self):
        print("pushbutton_6 pressed")
    
    @Slot()
    def profileBtnPressed(self): 
        print("profile button pressed")
    
    @Slot()
    def pushButtonPressed(self):
        print("pushbutton pressed")
    
    @Slot()
    def closeBtnPressed(self):
        print("close button pressed")
    
    @Slot()
    def restoreBtnPressed(self):
        print("restore button pressed")
        
    @Slot()
    def minimizeBtnPressed(self):
        print("minimize button pressed")
        
    @Slot()
    def infoBtnPressed(self):
        print("info button pressed")
        
        
    @Slot()
    def settingsBtnPressed(self):
        print("settings button pressed")
        
    @Slot()
    def reportBtnPressed(self):
        print("report button pressed")


    @Slot()
    def helpBtnPressed(self):
        print('help button pressed')
    
    @Slot()
    def menuBtnPressed(self):
        print("menu button pressed")
        
    @Slot()
    def homeBtnPressed(self):
        print("home button pressed")
        
    @Slot()
    def dataBtnPressed(self):
        print("data button pressed")
        
    
        
    
    


