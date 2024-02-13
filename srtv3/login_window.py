# Login View version 2
# Ui file for creating the LoginView class

import sys, os
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QSizePolicy
import login_icons_rc

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(931, 692)
        Form.setMinimumSize(QtCore.QSize(800, 600))
        
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(60, 50, 811, 600))
        self.widget.setMinimumSize(QtCore.QSize(800, 600))
        self.widget.setObjectName("widget")
        self.login_background = QtWidgets.QLabel(self.widget)
        self.login_background.setGeometry(QtCore.QRect(410, 60, 311, 421))
        sizePolicy = QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_background.sizePolicy().hasHeightForWidth())
        self.login_background.setSizePolicy(sizePolicy)
        self.login_background.setStyleSheet("background-color: rgb(202, 238, 236);\n"
"border-radius:10px;\n"
"")
        self.login_background.setText("")
        self.login_background.setObjectName("login_background")
        
        self.analytics_background = QtWidgets.QLabel(self.widget)
        self.analytics_background.setGeometry(QtCore.QRect(80, 40, 331, 461))
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.analytics_background.sizePolicy().hasHeightForWidth())
        
        self.analytics_background.setSizePolicy(sizePolicy)
        self.analytics_background.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(147, 251, 157, 255), stop:1 rgba(9, 199, 251, 255));\n"
"border-radius:10px;\n"
" \n"
"\n"
"")
        self.analytics_background.setText("")
        self.analytics_background.setScaledContents(False)
        self.analytics_background.setObjectName("analytics_background")
        
        self.logo_frame = QtWidgets.QFrame(self.widget)
        self.logo_frame.setGeometry(QtCore.QRect(410, 90, 311, 51))
        self.logo_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.logo_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.logo_frame.setObjectName("logo_frame")
        self.logo = QtWidgets.QLabel(self.logo_frame)
        self.logo.setGeometry(QtCore.QRect(130, 0, 45, 50))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/Logo/Logo/Stay Smart Logo 1.png"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logo.setObjectName("logo")
        self.analytics_logo = QtWidgets.QLabel(self.widget)
        self.analytics_logo.setGeometry(QtCore.QRect(130, 140, 221, 321))
        self.analytics_logo.setText("")
        self.analytics_logo.setPixmap(QtGui.QPixmap(":/Logo/Logo/7731130.png"))
        self.analytics_logo.setScaledContents(True)
        self.analytics_logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.analytics_logo.setObjectName("analytics_logo")
        self.layoutWidget = QtWidgets.QWidget(self.widget)
        self.layoutWidget.setGeometry(QtCore.QRect(450, 200, 231, 221))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setMaximumSize(QtCore.QSize(20, 20))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/IconsBlue/IconsBlue/#0088b9/user.svg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(125, 29))
        self.lineEdit.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:2px solid rgba(0, 0, 0, 0);\n"
"border-bottom-color:rgba(17, 243, 255, 255);\n"
"color:rgb(0, 0, 0);\n"
"padding-bottom:7px;")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pass_label = QtWidgets.QLabel(self.layoutWidget)
        self.pass_label.setMaximumSize(QtCore.QSize(20, 20))
        self.pass_label.setStyleSheet("color: rgb(12, 67, 112);")
        self.pass_label.setText("")
        self.pass_label.setPixmap(QtGui.QPixmap(":/IconsBlue/IconsBlue/#0088b9/key.svg"))
        self.pass_label.setScaledContents(True)
        self.pass_label.setObjectName("pass_label")
        self.horizontalLayout_2.addWidget(self.pass_label)
        self.password_input = QtWidgets.QLineEdit(self.layoutWidget)
        self.password_input.setMinimumSize(QtCore.QSize(125, 29))
        self.password_input.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:2px solid rgba(0, 0, 0, 0);\n"
"border-bottom-color:rgba(17, 243, 255, 255);\n"
"color:rgb(0, 0, 0);\n"
"padding-bottom:7px;")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_input.setObjectName("password_input")
        self.horizontalLayout_2.addWidget(self.password_input)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.remembeme_checkBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.remembeme_checkBox.setMaximumSize(QtCore.QSize(16777215, 29))
        self.remembeme_checkBox.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.remembeme_checkBox.setStyleSheet("color: rgb(53, 185, 223);\n"
"border-radius:10px;\n"
"padding:5px;\n"
"")
        self.remembeme_checkBox.setObjectName("remembeme_checkBox")
        self.verticalLayout.addWidget(self.remembeme_checkBox)
        self.login_button = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(True)
        self.login_button.setFont(font)
        self.login_button.setStyleSheet("QPushButton#login_button{\n"
"    color: rgb(0, 136, 185);\n"
"    border-radius:10px\n"
"}\n"
"\n"
"QPushButton#login_button:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-position:calc(100% - 10px)center;\n"
"}\n"
"\n"
"QPushButton#login_button:hover{\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"")
        self.login_button.setObjectName("login_button")
        self.verticalLayout.addWidget(self.login_button)
        self.forgot_button = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        self.forgot_button.setFont(font)
        self.forgot_button.setStyleSheet("QPushButton#forgot_button{\n"
"    color: rgb(0, 136, 185);\n"
"    border:0px solid rgba(0, 0, 0, 0);\n"
"}\n"
"\n"
"QPushButton#forgot_button:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-position:calc(100% - 10px)center;\n"
"}\n"
"\n"
"QPushButton#forgot_button:hover{\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.forgot_button.setObjectName("forgot_button")
        self.verticalLayout.addWidget(self.forgot_button)
        self.visibility_button = QtWidgets.QPushButton(self.widget)
        self.visibility_button.setGeometry(QtCore.QRect(680, 255, 26, 26))
        self.visibility_button.setMaximumSize(QtCore.QSize(26, 26))
        self.visibility_button.setStyleSheet("bottom-padding:5px;\n"
"border:2px;")
        self.visibility_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/IconsBlue/IconsBlue/#0088b9/eye-off.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon.addPixmap(QtGui.QPixmap(":/IconsBlue/IconsBlue/#0088b9/eye.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.visibility_button.setIcon(icon)
        self.visibility_button.setCheckable(True)
        self.visibility_button.setObjectName("visibility_button")
        self.login_background.raise_()
        self.layoutWidget.raise_()
        self.logo_frame.raise_()
        self.analytics_background.raise_()
        self.visibility_button.raise_()
        self.analytics_logo.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("SRT Login", "SRT Login"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Username"))
        self.password_input.setPlaceholderText(_translate("Form", "Password"))
        self.remembeme_checkBox.setText(_translate("Form", "  Remember Me"))
        self.login_button.setText(_translate("Form", "Login"))
        self.forgot_button.setText(_translate("Form", "Forgot Password?"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Form = QtWidgets.QWidget()
#     ui = Ui_Form()
#     ui.setupUi(Form)
#     Form.show()
#     sys.exit(app.exec_())
