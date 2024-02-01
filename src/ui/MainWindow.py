
import os
import sys

from PySide6 import QtGui, QtCore, QtWidgets
from resources import resources2
from tests.basic_table import TableModel, DataWindow, DF

from ui.main_ui_2 import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, user=None):
        super().__init__()
        self.user = user
        self.setupUi(self)
        self.setWindowTitle("StaySmart: Student Retention Tool")

        # Set the icon for the window
        main_window_icon = QtGui.QIcon()
        main_window_icon.addFile("resources/images/Stay Smart Logo 1.png")
        self.setWindowIcon(main_window_icon)

        # Prevent the extended icon menus from trying to both start up in the beginning
        self.iconsWithTextWidget.setHidden(True)

        # If either home button is clicked, switch to the home page
        self.homeButton.clicked.connect(self.switch_to_home_page)
        self.homeButtonWithText.clicked.connect(self.switch_to_home_page)

        # If either data analysis button is clicked, switch to the data analysis page
        self.dataAnalysisButton.clicked.connect(self.switch_to_data_analysis_page)
        self.dataAnalysisButtonWithText.clicked.connect(self.switch_to_data_analysis_page)

        # If either reports button is clicked, switch to the reports page
        self.reportsButton.clicked.connect(self.switch_to_report_page)
        self.reportsButtonWithText.clicked.connect(self.switch_to_report_page)

        # If either notifications button is clicked, switch to the notifications page
        self.notificationsButton.clicked.connect(self.switch_to_notifications_page)
        self.notificationsButtonWithText.clicked.connect(self.switch_to_notifications_page)

        # If either settings button is clicked, switch to the settings page
        self.settingsButton.clicked.connect(self.switch_to_settings_page)
        self.settingsButtonWithText.clicked.connect(self.switch_to_settings_page)


        
    # Define each page and its index within the stacked widget    
    def switch_to_home_page(self):
        self.stackedWidget.setCurrentIndex(0)  

    def switch_to_data_analysis_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_report_page(self):
        self.stackedWidget.setCurrentIndex(2) 

    def switch_to_notifications_page(self):
        self.stackedWidget.setCurrentIndex(3) 

    def switch_to_settings_page(self):
        self.stackedWidget.setCurrentIndex(4)


