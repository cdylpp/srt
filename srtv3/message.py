from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QRadioButton, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QVBoxLayout, QWidget)

class SettingsPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setupUi()
        self.radioDark.setChecked(True)
        # Connect the 'toggled' signal to changeTheme
        self.radioDark.toggled.connect(self.changeTheme)
        self.radioLight.toggled.connect(self.changeTheme)

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
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(300, 400)
        self.frame.setMaximumSize(350, 600)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

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

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)

        self.label_3 = QLabel("Contrast", self.frame)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3, 0, Qt.AlignTop)

        self.horizontalSlider = QSlider(self.frame)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setStyleSheet(
            "QSlider::handle {\n"
            "    background-color: rgb(22, 25, 29);\n"
            "}"
        )
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.verticalLayout.addWidget(self.horizontalSlider)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.pushButton = QPushButton("Restore Default Settings", self.frame)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet(
            "QPushButton{\n"
            "	background-color: rgb(22, 25, 29);\n"
            "}"
        )
        self.verticalLayout.addWidget(self.pushButton, 0, Qt.AlignTop | Qt.AlignHCenter)

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
        stylesheet_path = f"C:/Users/acarr/srt/src/resources/themes/{theme_name}.qss"
        try:
            with open(stylesheet_path, "r") as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
                if self.main_window:
                    self.main_window.setStyleSheet(stylesheet)
        except FileNotFoundError:
            print(f"Failed to load stylesheet: {stylesheet_path}")

'''
    def changeTheme(self, state):
        if state == Qt.Checked:
            if self.sender() == self.checkBox:
                self.checkBox_2.setChecked(False)
            elif self.sender() == self.checkBox_2:
                self.checkBox.setChecked(False)

        # Check the state of the checkboxes after the changes
        dark_checked = self.checkBox.isChecked()
        light_checked = self.checkBox_2.isChecked()

        if dark_checked:
            # Dark theme selected
            self.setStyleSheet(
                """
                background-color: rgb(44, 49, 60);
                QWidget {
                    background-color: rgb(44, 49, 60);
                    color: rgb(246, 247, 247);
                }
                QPushButton {
                    background-color: rgb(22, 25, 29);
                    color: white;
                    border: 2px solid rgb(60, 60, 60);
                    border-radius: 5px;
                }
                QLabel {
                    color: rgb(246, 247, 247);
                }
                """
            )
            if self.main_window:
                self.main_window.setStyleSheet(
                    "background-color: rgb(33, 33, 33);\n"
                    "color: rgb(246, 247, 247);\n"
                    ""
                )
        elif light_checked:
            # Light theme selected
            self.setStyleSheet(
                """
                background-color: rgb(246, 247, 247);
                QWidget {
                    background-color: rgb(246, 247, 247);
                    color: rgb(22, 25, 29);
                }
                QPushButton {
                    background-color: rgb(44, 49, 60);
                    color: white;
                    border: 2px solid rgb(60, 60, 60);
                    border-radius: 5px;
                }
                QLabel {
                    color: rgb(22, 25, 29);
                }
                """
            )
            if self.main_window:
                self.main_window.setStyleSheet(
                    "background-color: rgb(240, 240, 240);\n"
                    "color: rgb(33, 33, 33);\n"
                    ""
                )
'''