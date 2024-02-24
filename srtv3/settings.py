import sys
import qdarktheme

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QRadioButton, QFrame,
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QSpacerItem,
                             QVBoxLayout, QWidget, QMainWindow, QDialog, QListWidget)
from PyQt6.QtWidgets import QMessageBox


class SettingsView(QWidget):
    def __init__(self, user, app_data_manager, parent=None):
        super().__init__(parent)
        self.user = user
        self.app_data_manager = app_data_manager
        self.type = "SettingsView"
        self.setupUi()

        if self.user.get_role() == "Admin":
            self.create_account_unlock_button()
            self.unlock_button.clicked.connect(self.show_locked_accounts)
        # Load the saved theme preference
        # self.load_theme_preference()

    #def load_theme_preference(self):
        # self.apply_theme(self.theme_preference)

    #def save_theme_preference(self):
        # Need to write code here to save the users theme preference to another
        # file that will be called by the load_them_preference() method

    # Function to apply the selected theme
    def create_account_unlock_button(self):
        self.unlock_button = QPushButton("Account Unlock", self)
        self.unlock_button.clicked.connect(self.show_locked_accounts)

    def show_locked_accounts(self):
        locked_accounts = self.app_data_manager.get_locked_accounts()
        self.list_dialog = QDialog(self)
        self.list_dialog.setWindowTitle("Locked Accounts")

        layout = QVBoxLayout()
        self.list_widget = QListWidget()

        for account in locked_accounts:
            self.list_widget.addItem(account['username'])

        unlock_button = QPushButton("Unlock Account")
        unlock_button.clicked.connect(self.on_account_selected)

        layout.addWidget(self.list_widget)
        layout.addWidget(unlock_button)
        self.list_dialog.setLayout(layout)
        self.list_dialog.exec()

    def on_account_selected(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            username = selected_item.text()
            self.unlock_account(username)
            self.list_dialog.close()

    def unlock_account(self, username):
        self.app_data_manager.reset_account_lock(username)
        QMessageBox.information(self, "Account Unlocked", f"{username};s account has been unlocked.")

    def apply_theme(self, theme):
        if theme == 'dark':
            qdarktheme.setup_theme()
        else:
            qdarktheme.setup_theme("light")

    # Function to handle when the theme radio buttons are clicked
    def handle_theme_change(self):
        if self.radioDark.isChecked():
            self.theme_preference = 'dark'
        else:
            self.theme_preference = 'light'
        self.apply_theme(self.theme_preference)

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(758, 866)

        self.gridLayout_2 = QGridLayout(self)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.frame = QFrame(self)
        self.frame.setObjectName("frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(300, 400)
        self.frame.setMaximumSize(350, 600)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")

        self.groupBox = QGroupBox("Theme", self.frame)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.radioDark = QRadioButton("Dark", self.groupBox)
        self.radioDark.setObjectName("radioDark")
        self.horizontalLayout.addWidget(self.radioDark)

        self.radioLight = QRadioButton("Light", self.groupBox)
        self.radioLight.setObjectName("radioLight")
        self.horizontalLayout.addWidget(self.radioLight)

        self.groupBox.setLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)

        self.label_3 = QLabel("Contrast", self.frame)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3, 0, Qt.AlignmentFlag.AlignTop)

        self.horizontalSlider = QSlider(self.frame)
        self.horizontalSlider.setObjectName("horizontalSlider")
      
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)
        self.verticalLayout.addWidget(self.horizontalSlider)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.pushButton = QPushButton("Restore Default Settings", self.frame)
        self.pushButton.setObjectName("pushButton")
      
        self.verticalLayout.addWidget(self.pushButton, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)

        # Connect the radio buttons to the handle_theme_change function
        self.radioDark.toggled.connect(self.handle_theme_change)
        self.radioLight.toggled.connect(self.handle_theme_change)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("Settings")