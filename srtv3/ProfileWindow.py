# Form implementation generated from reading ui file 'profile_window.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1204, 902)
        self.profile = QtWidgets.QWidget(parent=Form)
        self.profile.setGeometry(QtCore.QRect(10, 40, 1171, 831))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profile.sizePolicy().hasHeightForWidth())
        self.profile.setSizePolicy(sizePolicy)
        self.profile.setStyleSheet("")
        self.profile.setObjectName("profile")
        self.frame = QtWidgets.QFrame(parent=self.profile)
        self.frame.setGeometry(QtCore.QRect(460, 0, 321, 821))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.profile_frame = QtWidgets.QFrame(parent=self.frame)
        self.profile_frame.setMinimumSize(QtCore.QSize(100, 100))
        self.profile_frame.setMaximumSize(QtCore.QSize(100, 100))
        self.profile_frame.setStyleSheet("QFrame {\n"

"    border-radius: 50%\n"
"}")
        self.profile_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.profile_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.profile_frame.setObjectName("profile_frame")
        self.addPic_button = QtWidgets.QPushButton(parent=self.profile_frame)
        self.addPic_button.setGeometry(QtCore.QRect(70, 70, 31, 31))
        self.addPic_button.setMinimumSize(QtCore.QSize(31, 31))
        self.addPic_button.setMaximumSize(QtCore.QSize(31, 31))
        self.addPic_button.setStyleSheet("QPushButton {\n"
"        font: 24pt \"Segoe UI\";\n"
"        border: none;\n"
"        background-color:none;\n"
"}")
        self.addPic_button.setCheckable(True)
        self.addPic_button.setObjectName("addPic_button")
        self.profile_pic = QtWidgets.QLabel(parent=self.profile_frame)
        self.profile_pic.setGeometry(QtCore.QRect(0, 0, 100, 100))
        self.profile_pic.setMinimumSize(QtCore.QSize(100, 100))
        self.profile_pic.setMaximumSize(QtCore.QSize(100, 100))
        self.profile_pic.setText("")
        self.profile_pic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.profile_pic.setObjectName("profile_pic")
        self.profile_pic.raise_()
        self.addPic_button.raise_()
        self.verticalLayout.addWidget(self.profile_frame, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.role = QtWidgets.QLabel(parent=self.frame)
        self.role.setMaximumSize(QtCore.QSize(16777215, 118))
        self.role.setStyleSheet("\n"
"font: 9pt \"Segoe UI\";")
        self.role.setText("")
        self.role.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.role.setObjectName("role")
        self.verticalLayout.addWidget(self.role)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.full_name = QtWidgets.QLabel(parent=self.frame)
        self.full_name.setStyleSheet("\n"
"font: 9pt \"Segoe UI\";")
        self.full_name.setText("")
        self.full_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.full_name.setObjectName("full_name")
        self.verticalLayout.addWidget(self.full_name)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.email = QtWidgets.QLabel(parent=self.frame)
        self.email.setStyleSheet("\n"
"font: 9pt \"Segoe UI\";")
        self.email.setText("")
        self.email.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.email.setObjectName("email")
        self.verticalLayout.addWidget(self.email)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.contactInfo_button = QtWidgets.QPushButton(parent=self.frame)
        self.contactInfo_button.setStyleSheet("border:none;\n"
"font: 700 9pt \"Segoe UI\";")
        self.contactInfo_button.setObjectName("contactInfo_button")
        self.verticalLayout.addWidget(self.contactInfo_button)
        self.contactInfo_groupBox = QtWidgets.QGroupBox(parent=self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contactInfo_groupBox.sizePolicy().hasHeightForWidth())
        self.contactInfo_groupBox.setSizePolicy(sizePolicy)
        self.contactInfo_groupBox.setMinimumSize(QtCore.QSize(241, 91))
        self.contactInfo_groupBox.setStyleSheet("QLabel {\n"
"    font: 700 9pt \"Segoe UI\";\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton{\n"
"    font: 700;\n"
"}\n"
"\n"
"")
        self.contactInfo_groupBox.setTitle("")
        self.contactInfo_groupBox.setObjectName("contactInfo_groupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.contactInfo_groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 301, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.contactheader_horLayout = QtWidgets.QHBoxLayout()
        self.contactheader_horLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.contactheader_horLayout.setObjectName("contactheader_horLayout")
        self.phoneNum_label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phoneNum_label.sizePolicy().hasHeightForWidth())
        self.phoneNum_label.setSizePolicy(sizePolicy)
        self.phoneNum_label.setIndent(5)
        self.phoneNum_label.setObjectName("phoneNum_label")
        self.contactheader_horLayout.addWidget(self.phoneNum_label)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.contactheader_horLayout.addItem(spacerItem5)
        self.type_label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.type_label.sizePolicy().hasHeightForWidth())
        self.type_label.setSizePolicy(sizePolicy)
        self.type_label.setObjectName("type_label")
        self.contactheader_horLayout.addWidget(self.type_label)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.contactheader_horLayout.addItem(spacerItem6)
        self.preferred_label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preferred_label.sizePolicy().hasHeightForWidth())
        self.preferred_label.setSizePolicy(sizePolicy)
        self.preferred_label.setObjectName("preferred_label")
        self.contactheader_horLayout.addWidget(self.preferred_label)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.contactheader_horLayout.addItem(spacerItem7)
        self.verticalLayout_2.addLayout(self.contactheader_horLayout)
        self.row1_horLayout = QtWidgets.QHBoxLayout()
        self.row1_horLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.row1_horLayout.setObjectName("row1_horLayout")
        self.phone_number = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phone_number.sizePolicy().hasHeightForWidth())
        self.phone_number.setSizePolicy(sizePolicy)
        self.phone_number.setMinimumSize(QtCore.QSize(80, 48))
        self.phone_number.setMaximumSize(QtCore.QSize(80, 48))
        self.phone_number.setStyleSheet("font: 9pt \"Segoe UI\";")
        self.phone_number.setText("254-658-1236")
        self.phone_number.setIndent(5)
        self.phone_number.setObjectName("phone_number")
        self.row1_horLayout.addWidget(self.phone_number)
        spacerItem8 = QtWidgets.QSpacerItem(25, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.row1_horLayout.addItem(spacerItem8)
        self.comboBox = QtWidgets.QComboBox(parent=self.verticalLayoutWidget)
        self.comboBox.setMaximumSize(QtCore.QSize(77, 16777215))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.setItemText(0, "")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.row1_horLayout.addWidget(self.comboBox)
        spacerItem9 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.row1_horLayout.addItem(spacerItem9)
        self.checkBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget)
        self.checkBox.setMaximumSize(QtCore.QSize(20, 16777215))
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.row1_horLayout.addWidget(self.checkBox)
        spacerItem10 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.row1_horLayout.addItem(spacerItem10)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.verticalLayout_3.setContentsMargins(-1, -1, 2, -1)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.addcontact_button = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.addcontact_button.setMaximumSize(QtCore.QSize(20, 20))
        self.addcontact_button.setObjectName("addcontact_button")
        self.verticalLayout_3.addWidget(self.addcontact_button)
        self.delcontact_button = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.delcontact_button.setMaximumSize(QtCore.QSize(20, 20))
        self.delcontact_button.setObjectName("delcontact_button")
        self.verticalLayout_3.addWidget(self.delcontact_button)
        self.row1_horLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.row1_horLayout)
        self.verticalLayout.addWidget(self.contactInfo_groupBox)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem11)
        self.changePass_button = QtWidgets.QPushButton(parent=self.frame)
        self.changePass_button.setStyleSheet("border:none;\n"
"font: 700 9pt \"Segoe UI\";")
        self.changePass_button.setObjectName("changePass_button")
        self.verticalLayout.addWidget(self.changePass_button)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem12)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.addPic_button.setText(_translate("Form", "+"))
        self.contactInfo_button.setText(_translate("Form", "Contact Information"))
        self.phoneNum_label.setText(_translate("Form", "Phone Number"))
        self.type_label.setText(_translate("Form", "Type"))
        self.preferred_label.setText(_translate("Form", "Preferred"))
        self.comboBox.setItemText(1, _translate("Form", "Mobile"))
        self.comboBox.setItemText(2, _translate("Form", "Home"))
        self.comboBox.setItemText(3, _translate("Form", "Work"))
        self.addcontact_button.setText(_translate("Form", "+"))
        self.delcontact_button.setText(_translate("Form", "-"))
        self.changePass_button.setText(_translate("Form", "Change Password"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
