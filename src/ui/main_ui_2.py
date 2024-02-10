# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_ui_2.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

from tests.DataAnalysisPage import DataAnalysisPage
from tests.settings import SettingsPage


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(830, 600)
        MainWindow.setMinimumSize(QSize(800, 600))
        MainWindow.setStyleSheet(u"background-color: rgb(44, 49, 60);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.iconsWidget = QWidget(self.centralwidget)
        self.iconsWidget.setObjectName(u"iconsWidget")
        self.iconsWidget.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(22, 25, 29);\n"
"}\n"
"\n"
"QPushButton{\n"
"	color: white;\n"
"	height: 40px;\n"
"	border: none;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	background-color: rgb(44, 49, 60);\n"
"	font-weight: bold;\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.iconsWidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.staySmartLogo = QLabel(self.iconsWidget)
        self.staySmartLogo.setObjectName(u"staySmartLogo")
        self.staySmartLogo.setMinimumSize(QSize(45, 50))
        self.staySmartLogo.setMaximumSize(QSize(40, 50))
        self.staySmartLogo.setPixmap(QPixmap(u":/Logo/Logo/Stay Smart Logo 1.png"))
        self.staySmartLogo.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.staySmartLogo)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 15, -1, -1)
        self.homeButton = QPushButton(self.iconsWidget)
        self.homeButton.setObjectName(u"homeButton")
        icon = QIcon()
        icon.addFile(u":/Icons/home.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.homeButton.setIcon(icon)
        self.homeButton.setIconSize(QSize(24, 24))
        self.homeButton.setCheckable(True)
        self.homeButton.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.homeButton)

        self.dataAnalysisButton = QPushButton(self.iconsWidget)
        self.dataAnalysisButton.setObjectName(u"dataAnalysisButton")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/database.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.dataAnalysisButton.setIcon(icon1)
        self.dataAnalysisButton.setIconSize(QSize(24, 24))
        self.dataAnalysisButton.setCheckable(True)
        self.dataAnalysisButton.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.dataAnalysisButton)

        self.reportsButton = QPushButton(self.iconsWidget)
        self.reportsButton.setObjectName(u"reportsButton")
        icon2 = QIcon()
        icon2.addFile(u":/Icons/clipboard.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.reportsButton.setIcon(icon2)
        self.reportsButton.setIconSize(QSize(24, 24))
        self.reportsButton.setCheckable(True)
        self.reportsButton.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.reportsButton)

        self.notificationsButton = QPushButton(self.iconsWidget)
        self.notificationsButton.setObjectName(u"notificationsButton")
        icon3 = QIcon()
        icon3.addFile(u":/Icons/message-square.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.notificationsButton.setIcon(icon3)
        self.notificationsButton.setIconSize(QSize(24, 24))
        self.notificationsButton.setCheckable(True)
        self.notificationsButton.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.notificationsButton)

        self.settingsButton = QPushButton(self.iconsWidget)
        self.settingsButton.setObjectName(u"settingsButton")
        icon4 = QIcon()
        icon4.addFile(u":/Icons/settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsButton.setIcon(icon4)
        self.settingsButton.setIconSize(QSize(24, 24))
        self.settingsButton.setCheckable(True)
        self.settingsButton.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.settingsButton)

        self.verticalSpacer = QSpacerItem(20, 258, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.signOutButton = QPushButton(self.iconsWidget)
        self.signOutButton.setObjectName(u"signOutButton")
        icon5 = QIcon()
        icon5.addFile(u":/Icons/log-out.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.signOutButton.setIcon(icon5)
        self.signOutButton.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.signOutButton)


        self.verticalLayout_3.addLayout(self.verticalLayout)


        self.gridLayout.addWidget(self.iconsWidget, 0, 0, 1, 1)

        self.mainWidget = QWidget(self.centralwidget)
        self.mainWidget.setObjectName(u"mainWidget")
        self.verticalLayout_5 = QVBoxLayout(self.mainWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(2, 10, 10, 10)
        self.header_widget = QWidget(self.mainWidget)
        self.header_widget.setObjectName(u"header_widget")
        self.header_widget.setStyleSheet(u"background-color: rgb(22, 25, 29);\n"
"border: none;\n"
"")
        self.horizontalLayout_4 = QHBoxLayout(self.header_widget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(10, 15, 10, 15)
        self.collapseAndExpandButton = QPushButton(self.header_widget)
        self.collapseAndExpandButton.setObjectName(u"collapseAndExpandButton")
        icon6 = QIcon()
        icon6.addFile(u":/Icons/menu.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.collapseAndExpandButton.setIcon(icon6)
        self.collapseAndExpandButton.setIconSize(QSize(24, 24))
        self.collapseAndExpandButton.setCheckable(True)
        self.collapseAndExpandButton.setAutoExclusive(False)

        self.horizontalLayout_4.addWidget(self.collapseAndExpandButton)

        self.horizontalSpacer_2 = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.searchBar = QLineEdit(self.header_widget)
        self.searchBar.setObjectName(u"searchBar")
        self.searchBar.setMinimumSize(QSize(200, 24))
        self.searchBar.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout.addWidget(self.searchBar)

        self.searchButton = QPushButton(self.header_widget)
        self.searchButton.setObjectName(u"searchButton")
        icon7 = QIcon()
        icon7.addFile(u":/Icons/search.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.searchButton.setIcon(icon7)
        self.searchButton.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.searchButton)


        self.horizontalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.profileButton = QPushButton(self.header_widget)
        self.profileButton.setObjectName(u"profileButton")
        self.profileButton.setAutoFillBackground(False)
        self.profileButton.setStyleSheet(u"border-radius: 40px;")
        icon8 = QIcon()
        icon8.addFile(u":/Icons/user.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.profileButton.setIcon(icon8)
        self.profileButton.setIconSize(QSize(24, 24))

        self.horizontalLayout_4.addWidget(self.profileButton)


        self.verticalLayout_5.addWidget(self.header_widget)

        self.stackedWidget = QStackedWidget(self.mainWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background-color: rgb(44, 49, 60);\n"
"color: white;")
        
        self.homePage = QWidget()
        self.homePage.setObjectName(u"homePage")
        self.placeholderTextForHomePage = QLabel(self.homePage)
        self.placeholderTextForHomePage.setObjectName(u"placeholderTextForHomePage")
        self.placeholderTextForHomePage.setGeometry(QRect(200, 210, 171, 81))
        font = QFont()
        font.setPointSize(20)
        self.placeholderTextForHomePage.setFont(font)
        self.stackedWidget.addWidget(self.homePage)

        # Place Holder for Custom Widget
        self.dataAnalysisPage = DataAnalysisPage()
        self.dataAnalysisPage.setObjectName(u"dataAnalysisPage")
        self.stackedWidget.addWidget(self.dataAnalysisPage)
        
        self.reportsPage = QWidget()
        self.reportsPage.setObjectName(u"reportsPage")
        self.placeholderTextForReportsPage = QLabel(self.reportsPage)
        self.placeholderTextForReportsPage.setObjectName(u"placeholderTextForReportsPage")
        self.placeholderTextForReportsPage.setGeometry(QRect(200, 200, 171, 81))
        self.placeholderTextForReportsPage.setFont(font)
        self.stackedWidget.addWidget(self.reportsPage)
        
        self.notificationsPage = QWidget()
        self.notificationsPage.setObjectName(u"notificationsPage")
        self.placeholderTextForNotificationsPage = QLabel(self.notificationsPage)
        self.placeholderTextForNotificationsPage.setObjectName(u"placeholderTextForNotificationsPage")
        self.placeholderTextForNotificationsPage.setGeometry(QRect(160, 200, 251, 81))
        self.placeholderTextForNotificationsPage.setFont(font)
        self.stackedWidget.addWidget(self.notificationsPage)

        self.settingsPage = SettingsPage()
        self.stackedWidget.addWidget(self.settingsPage)

        self.verticalLayout_5.addWidget(self.stackedWidget)


        self.gridLayout.addWidget(self.mainWidget, 0, 2, 1, 1)

        self.iconsWithTextWidget = QWidget(self.centralwidget)
        self.iconsWithTextWidget.setObjectName(u"iconsWithTextWidget")
        self.iconsWithTextWidget.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(22, 25, 29);\n"
"	color: white;\n"
"}\n"
"\n"
"QPushButton{\n"
"	color: white;\n"
"	text-align: left;\n"
"	height: 40px;\n"
"	padding-left: 10px;\n"
"	border: none;\n"
"	border-top-left-radius: 10px;\n"
"	border-bottom-left-radius: 10px\n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	background-color: rgb(44, 49, 60);\n"
"	font-weight: bold;\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.iconsWithTextWidget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, 20, -1)
        self.staySmartLogoWithText = QLabel(self.iconsWithTextWidget)
        self.staySmartLogoWithText.setObjectName(u"staySmartLogoWithText")
        self.staySmartLogoWithText.setMinimumSize(QSize(45, 50))
        self.staySmartLogoWithText.setMaximumSize(QSize(45, 50))
        self.staySmartLogoWithText.setPixmap(QPixmap(u":/images/Stay Smart Logo 1.png"))
        self.staySmartLogoWithText.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.staySmartLogoWithText)

        self.staySmartText = QLabel(self.iconsWithTextWidget)
        self.staySmartText.setObjectName(u"staySmartText")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.staySmartText.setFont(font1)

        self.horizontalLayout_2.addWidget(self.staySmartText)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 15, -1, -1)
        self.homeButtonWithText = QPushButton(self.iconsWithTextWidget)
        self.homeButtonWithText.setObjectName(u"homeButtonWithText")
        font2 = QFont()
        font2.setPointSize(12)
        self.homeButtonWithText.setFont(font2)
        self.homeButtonWithText.setIcon(icon)
        self.homeButtonWithText.setIconSize(QSize(24, 24))
        self.homeButtonWithText.setCheckable(True)
        self.homeButtonWithText.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.homeButtonWithText)

        self.dataAnalysisButtonWithText = QPushButton(self.iconsWithTextWidget)
        self.dataAnalysisButtonWithText.setObjectName(u"dataAnalysisButtonWithText")
        self.dataAnalysisButtonWithText.setFont(font2)
        self.dataAnalysisButtonWithText.setIcon(icon1)
        self.dataAnalysisButtonWithText.setIconSize(QSize(24, 24))
        self.dataAnalysisButtonWithText.setCheckable(True)
        self.dataAnalysisButtonWithText.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.dataAnalysisButtonWithText)

        self.reportsButtonWithText = QPushButton(self.iconsWithTextWidget)
        self.reportsButtonWithText.setObjectName(u"reportsButtonWithText")
        self.reportsButtonWithText.setFont(font2)
        self.reportsButtonWithText.setIcon(icon2)
        self.reportsButtonWithText.setIconSize(QSize(24, 24))
        self.reportsButtonWithText.setCheckable(True)
        self.reportsButtonWithText.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.reportsButtonWithText)

        self.notificationsButtonWithText = QPushButton(self.iconsWithTextWidget)
        self.notificationsButtonWithText.setObjectName(u"notificationsButtonWithText")
        self.notificationsButtonWithText.setFont(font2)
        self.notificationsButtonWithText.setIcon(icon3)
        self.notificationsButtonWithText.setIconSize(QSize(24, 24))
        self.notificationsButtonWithText.setCheckable(True)
        self.notificationsButtonWithText.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.notificationsButtonWithText)

        self.settingsButtonWithText = QPushButton(self.iconsWithTextWidget)
        self.settingsButtonWithText.setObjectName(u"settingsButtonWithText")
        self.settingsButtonWithText.setFont(font2)
        self.settingsButtonWithText.setIcon(icon4)
        self.settingsButtonWithText.setIconSize(QSize(24, 24))
        self.settingsButtonWithText.setCheckable(True)
        self.settingsButtonWithText.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.settingsButtonWithText)

        self.verticalSpacer_2 = QSpacerItem(20, 258, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.signOutButtonWithText = QPushButton(self.iconsWithTextWidget)
        self.signOutButtonWithText.setObjectName(u"signOutButtonWithText")
        self.signOutButtonWithText.setFont(font2)
        self.signOutButtonWithText.setIcon(icon5)
        self.signOutButtonWithText.setIconSize(QSize(24, 24))

        self.verticalLayout_2.addWidget(self.signOutButtonWithText)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)


        self.gridLayout.addWidget(self.iconsWithTextWidget, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.collapseAndExpandButton.toggled.connect(self.iconsWidget.setHidden)
        self.collapseAndExpandButton.toggled.connect(self.iconsWithTextWidget.setVisible)
        self.settingsButton.toggled.connect(self.settingsButtonWithText.setChecked)
        self.notificationsButton.toggled.connect(self.notificationsButtonWithText.setChecked)
        self.reportsButton.toggled.connect(self.reportsButtonWithText.setChecked)
        self.dataAnalysisButton.toggled.connect(self.dataAnalysisButtonWithText.setChecked)
        self.homeButton.toggled.connect(self.homeButtonWithText.setChecked)
        self.homeButtonWithText.toggled.connect(self.homeButton.setChecked)
        self.dataAnalysisButtonWithText.toggled.connect(self.dataAnalysisButton.setChecked)
        self.reportsButtonWithText.toggled.connect(self.reportsButton.setChecked)
        self.notificationsButtonWithText.toggled.connect(self.notificationsButton.setChecked)
        self.settingsButtonWithText.toggled.connect(self.settingsButton.setChecked)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.staySmartLogo.setText("")
        self.homeButton.setText("")
        self.dataAnalysisButton.setText("")
        self.reportsButton.setText("")
        self.notificationsButton.setText("")
        self.settingsButton.setText("")
        self.signOutButton.setText("")
        self.collapseAndExpandButton.setText("")
        self.searchButton.setText("")
        self.profileButton.setText("")
        self.placeholderTextForHomePage.setText(QCoreApplication.translate("MainWindow", u"Home Page", None))
        # self.placeholderTextForDataAnalysisPage.setText(QCoreApplication.translate("MainWindow", u"Data Analysis Page", None))
        self.placeholderTextForReportsPage.setText(QCoreApplication.translate("MainWindow", u"Reports Page", None))
        # self.placeholderTextForSettingsPage.setText(QCoreApplication.translate("MainWindow", u"Notifications Page", None))
        #self.placeholderTextForNotificationsPage.setText(QCoreApplication.translate("MainWindow", u"Settings Page", None))
        self.staySmartLogoWithText.setText("")
        self.staySmartText.setText(QCoreApplication.translate("MainWindow", u"StaySmart", None))
        self.homeButtonWithText.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.dataAnalysisButtonWithText.setText(QCoreApplication.translate("MainWindow", u"Data Analysis", None))
        self.reportsButtonWithText.setText(QCoreApplication.translate("MainWindow", u"Reports", None))
        self.notificationsButtonWithText.setText(QCoreApplication.translate("MainWindow", u"Notifications", None))
        self.settingsButtonWithText.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.signOutButtonWithText.setText(QCoreApplication.translate("MainWindow", u"Sign Out", None))
    # retranslateUi

