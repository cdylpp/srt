import os
import sys

from PyQt6.QtWidgets import QMessageBox
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtGui import QCloseEvent
from resources import resources2

from ui.main_ui_2 import Ui_MainWindow
# from ui.main_gui_blue import Ui_MainWindow # from ui.main_ui_2 import Ui_MainWindow
from ui.LoginWindow import LoginWindow
from tests.settings import SettingsPage
from tests.user import UserManager

current_dir = os.path.dirname(os.path.abspath(__file__))

resources_dir = os.path.join(current_dir, '..', 'resources')
sys.path.append(resources_dir)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    main_window_closed = QtCore.Signal()

    def __init__(self, user_manager=None, app_data=None):
        super().__init__()
        self.user_manager = user_manager
        self.app_data = app_data
        self.user = self.user_manager.get_user()
        self.setupUi(self)
        self.setWindowTitle(f"StaySmart: Student Retention Tool - {self.user.get_name()}")

        # Set the icon for the window
        main_window_icon = QtGui.QIcon()
        main_window_icon.addFile(":/Logo/Logo/Stay Smart Logo 1.png")  #resources/images/Stay Smart Logo 1.png
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

        # If sign out button is clicked, sign out
        self.signOutButton.clicked.connect(self.on_sign_out)
        self.signOutButtonWithText.clicked.connect(self.on_sign_out)

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

    def on_sign_out(self):
        # Ask for confirmation
        reply = QMessageBox.question(None, 'Confirmation', 'Are you sure you want to sign out?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # Close the current window
            self.close()

            # Open a new instance of LoginDialog
            login_window = LoginWindow('mysql', db_url=os.getenv("DB_URL"), app_data=self.app_data) #login_dialog = LoginDialog
            login_window.exec() #login_dialog.exec()
        # TODO: The login needs to take the user back to the Main App after signing in.
        # This might have to be implemented in the SrtApp which is the QApplication class.
    
    # Method to handle closed window
    def closeEvent(self, event: QCloseEvent) -> None:
        self.main_window_closed.emit()
        event.accept()
        return


