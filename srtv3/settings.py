import sys, os

from PyQt6.QtCore import QCoreApplication, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QApplication, QRadioButton, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QVBoxLayout, QWidget, QMainWindow)

class SettingsView(QWidget):
    def __init__(self, parent: QWidget, main: QMainWindow):
        super().__init__(parent)
        self.type = "SettingsPage"
        self.main = main
        self.setupUi()
        self.radioDark.setChecked(True)
        # Connect the 'toggled' signal to changeTheme
        self.radioDark.toggled.connect(self.changeTheme)

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(758, 866)
        self.setStyleSheet(
            "background-color: rgb(44, 49, 60);\n"
            "color: rgb(246, 247, 247);\n"
        )

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
        self.horizontalSlider.setStyleSheet(
            "QSlider::handle {\n"
            "    background-color: rgb(22, 25, 29);\n"
            "}"
        )
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)
        self.verticalLayout.addWidget(self.horizontalSlider)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.pushButton = QPushButton("Restore Default Settings", self.frame)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet(
            "QPushButton{\n"
            "	background-color: rgb(22, 25, 29);\n"
            "}"
        )
        self.verticalLayout.addWidget(self.pushButton, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Form", "Form", None))

    def changeTheme(self):
        if self.radioDark.isChecked():
            self.applyDarkTheme()
        elif self.radioLight.isChecked():
            self.applyLightTheme()

    def applyDarkTheme(self):
        self.loadStyleSheet("darktheme")

    def applyLightTheme(self):
        self.loadStyleSheet("lighttheme")

    def loadStyleSheet(self, theme_name):
        # Assuming the .qss files are stored in "C:/Users/acarr/srt/src/resources/themes/"
        # current_directory = os.getcwd()
        # stylesheet_path = os.path.join(current_directory, f"data/{theme_name}.qss")
        # try:
        #     with open(stylesheet_path, "r") as file:
        #         print(f"Changed the settings: {theme_name}")
        #         styleSheet = str(file)
        #         self.setStyleSheet(styleSheet)
        #         # stylesheet = file.read()
        #         # self.setStyleSheet(stylesheet)
        #         # if self.main_window:
        #         #     self.main_window.setStyleSheet(stylesheet)
        # except FileNotFoundError:
        #     print(f"Failed to load stylesheet: {stylesheet_path}")

        if theme_name == 'lighttheme':
            self.setStyleSheet(
                "background-color: rgb(246, 246, 246);\n"
            )

        elif theme_name == 'darktheme':
            self.setStyleSheet(
                "background-color: rgb(30, 30, 30);\n"
            )
        else:
            print("Style not supported.")


