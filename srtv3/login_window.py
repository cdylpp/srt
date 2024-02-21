from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)
import login_icons_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"StaySmart: Student Retention Tool")
        Form.resize(800, 600)
        Form.setMinimumSize(QSize(800, 600))
        Form.setMaximumSize(QSize(800, 600))
        Form.setStyleSheet(u"background-color: rgb(52, 53, 65);\n"
"\n"
"QLabel {\n"
"    color: white;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background-color: white;\n"
"}\n"
"\n"
"QPushButton {\n"
"    color: white;\n"
"}\n"
"")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 800, 600))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(800, 600))
        self.widget.setMaximumSize(QSize(800, 600))
        self.widget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.widget.setStyleSheet(u"background-color: rgb(52, 53, 65);\n"
"\n"
"QLabel {\n"
"    color: white;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background-color: white;\n"
"}\n"
"\n"
"QPushButton {\n"
"    color: white;\n"
"}")
        self.gridLayout_4 = QGridLayout(self.widget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.widget_2.setMinimumSize(QSize(300, 400))
        self.widget_2.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"border-radius: 20px")
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.logo_frame = QFrame(self.widget_2)
        self.logo_frame.setObjectName(u"logo_frame")
        sizePolicy1.setHeightForWidth(self.logo_frame.sizePolicy().hasHeightForWidth())
        self.logo_frame.setSizePolicy(sizePolicy1)
        self.logo_frame.setMinimumSize(QSize(300, 100))
        self.logo_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.logo_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.logo_frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.logo = QLabel(self.logo_frame)
        self.logo.setObjectName(u"logo")
        sizePolicy1.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy1)
        self.logo.setMinimumSize(QSize(105, 120))
        self.logo.setMaximumSize(QSize(105, 120))
        self.logo.setPixmap(QPixmap(u":/Logo/Logo/Stay Smart Logo 1.png"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.logo, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.logo_frame, 0, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(35, 0, 35, 20)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(20, 20))
        self.label.setPixmap(QPixmap("srtv3/Icons/user.svg"))
        self.label.setScaledContents(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.lineEdit = QLineEdit(self.widget_2)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy1.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy1)
        self.lineEdit.setMinimumSize(QSize(180, 29))
        self.lineEdit.setStyleSheet(u"background-color: white;\n"
"border:2px solid rgba(0, 0, 0, 0);\n"
"border-bottom-color:rgba(17, 243, 255, 255);\n"
"color:rgb(0, 0, 0);\n"
"padding-bottom:7px;")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEdit)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pass_label = QLabel(self.widget_2)
        self.pass_label.setObjectName(u"pass_label")
        self.pass_label.setMaximumSize(QSize(20, 20))
        self.pass_label.setStyleSheet(u"color: rgb(12, 67, 112);")
        self.pass_label.setPixmap(QPixmap("srtv3/Icons/key.svg"))
        self.pass_label.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.pass_label)

        self.password_input = QLineEdit(self.widget_2)
        self.password_input.setObjectName(u"password_input")
        self.password_input.setMinimumSize(QSize(180, 29))
        self.password_input.setStyleSheet(u"background-color: white;\n"
"border:2px solid rgba(0, 0, 0, 0);\n"
"border-bottom-color:rgba(17, 243, 255, 255);\n"
"color:rgb(0, 0, 0);\n"
"padding-bottom:7px;")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.horizontalLayout_2.addWidget(self.password_input)

        self.visibility_button = QPushButton(self.widget_2)
        self.visibility_button.setObjectName(u"visibility_button")
        self.visibility_button.setMaximumSize(QSize(26, 26))
        self.visibility_button.setStyleSheet(u"bottom-padding:5px;\n"
"border:2px;")
        icon = QIcon()
        icon.addFile("srtv3\Icons\eye-off.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon.addFile("srtv3\Icons\eye.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.visibility_button.setIcon(icon)
        self.visibility_button.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.visibility_button)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.remembeme_checkBox = QCheckBox(self.widget_2)
        self.remembeme_checkBox.setObjectName(u"remembeme_checkBox")
        self.remembeme_checkBox.setMaximumSize(QSize(16777215, 29))
        self.remembeme_checkBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.remembeme_checkBox.setStyleSheet(u"color: white;\n"
"border-radius:10px;\n"
"padding:0px;\n"
"")

        self.verticalLayout.addWidget(self.remembeme_checkBox, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.login_button = QPushButton(self.widget_2)
        self.login_button.setObjectName(u"login_button")
        font = QFont()
        font.setPointSize(19)
        font.setBold(True)
        self.login_button.setFont(font)
        self.login_button.setStyleSheet(u"QPushButton#login_button{\n"
"	color: white;\n"
"	border-radius:10px\n"
"}\n"
"\n"
"QPushButton#login_button:pressed{\n"
"	padding-left:5px;\n"
"	padding-top:5px;\n"
"	background-position:calc(100% - 10px)center;\n"
"}\n"
"\n"
"QPushButton#login_button:hover{\n"
"	\n"
"	color: rgb(223, 223, 223);\n"
"}\n"
"\n"
"")

        self.verticalLayout.addWidget(self.login_button, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.forgot_button = QPushButton(self.widget_2)
        self.forgot_button.setObjectName(u"forgot_button")
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(True)
        self.forgot_button.setFont(font1)
        self.forgot_button.setStyleSheet(u"QPushButton#forgot_button{\n"
"	color: white;\n"
"	border:0px solid rgba(0, 0, 0, 0);\n"
"}\n"
"\n"
"QPushButton#forgot_button:pressed{\n"
"	padding-left:5px;\n"
"	padding-top:5px;\n"
"	background-position:calc(100% - 10px)center;\n"
"}\n"
"\n"
"QPushButton#forgot_button:hover{\n"
"	color: rgb(223, 223, 223);\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.forgot_button, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)


        self.gridLayout_4.addWidget(self.widget_2, 0, 0, 1, 1)

        self.layoutWidget = QWidget(Form)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 2, 2))
        self.gridLayout_2 = QGridLayout(self.layoutWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle("StaySmart: Student Retention Tool")
        self.logo.setText("")
        self.label.setText("")
        self.lineEdit.setPlaceholderText("Username")
        self.pass_label.setText("")
        self.password_input.setPlaceholderText("Password")
        self.visibility_button.setText("")
        self.remembeme_checkBox.setText("Remember Me")
        self.login_button.setText("Login")
        self.forgot_button.setText("Forgot Password?")

    # retranslateUi

