# DataAnalysisPage is the view that is under the Data Analysis tab
# This view should control and maintain all interactions within the Data Analysis Tab
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QTabWidget, 
    QToolBar, QProgressBar, QStatusBar, QVBoxLayout, QFileDialog, QWidget, 
    QHBoxLayout, QVBoxLayout, QScrollArea, QTextBrowser, QDockWidget, QPushButton, QTableView,
    QMessageBox, QGridLayout, QFrame, QGroupBox, QRadioButton,QSpacerItem, QSizePolicy, QSlider)

from PyQt6.QtCore import QSize, pyqtSignal, Qt, pyqtSlot, QCoreApplication
from PyQt6.QtGui import QIcon, QAction, QPixmap

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from widgets import (
    TreeWidgetFactory, TableView, 
    ControlDockTabWidget, ModellingController)

from user import User
from models import TableModel, MarkdownModel
from paths import Paths
from pandas import read_csv
import pyqtgraph as pg
from utils import detect_csv_separator, path_to_title, Transformer
from ProfileWindow import Ui_Form


style_sheet = """
    QTabWidget:pane{
        border: none
    }
"""

class MainWindow(QMainWindow):

    browser_closed = pyqtSignal()

    def __init__(self, user_manager=None, app_data=None):
        super().__init__()
        self.user_manager = None
        self.app_data = app_data
        self.user = user_manager.get_user()
        self.model = None

        self.views = []
        self.plot_views = {}
        self.controllers = {}

        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(300, 200)
        # Title
        self.setWindowTitle(f"Student Retention Analysis - {self.user.get_name()}")
        self.setWindowIcon(
            QIcon(Paths.icon("Stay Smart Logo 1.png"))
        )

        self.sizeMainWindow() 
        self.create_toolbar()
        self.setup_main_window()
        self.create_actions()
        self.create_menu()

        # change the tab to index 0
        self.on_tab_switch(0)
        self.show()

    def setup_main_window(self):
        """Create the QTabWidget object and the different pages
        for the main window. Handle when a tab is closed."""

        self.tab_bar = QTabWidget()
        self.tab_bar.setTabsClosable(True) # Add close buttons to tabs
        self.tab_bar.setTabBarAutoHide(True) # Hides tab bar when less than 2 tabs
        self.tab_bar.tabCloseRequested.connect(self.on_close_tab) # signal to on_close_tab
        self.tab_bar.currentChanged.connect(self.on_tab_switch)

        self.create_dock_widgets()

        # Create Welcome View
        self.main_tab = self.handle_markdown('srtv3/Welcome.md')
        # self.tab_bar.addTab(self.main_tab, "Welcome")

        # Call method that sets up each page
        # self.setUpTab(self.main_tab)
        self.setCentralWidget(self.tab_bar)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def create_actions(self):
        """Create the application's menu actions."""
        # Create actions for File menu   
        self.new_window_action = QAction("New Window", self)
        self.new_window_action.setShortcut("Ctrl+N")
        self.new_window_action.triggered.connect(self.on_new_window)

        self.new_tab_action = QAction("New Tab", self)
        self.new_tab_action.setShortcut("Ctrl+T")
        self.new_tab_action.triggered.connect(self.on_new_tab)

        self.quit_action = QAction("Quit Browser", self)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.close)

        self.import_action = QAction("Import Data", self)
        self.import_action.setShortcut("Ctrl+O")
        self.import_action.triggered.connect(self.on_import)

        # Create actions for Analysis menu
        self.describe_action = QAction("Describe", self)
        self.describe_action.setShortcut("Ctrl+D")
        self.describe_action.triggered.connect(self.on_describe_action)

        self.info_action = QAction("Information", self)
        self.info_action.setShortcut("Ctrl+I")
        self.info_action.triggered.connect(self.on_info_action)

        self.plot_action = QAction("Plot Data",self)
        self.plot_action.setShortcut("Ctrl+P")
        self.plot_action.triggered.connect(self.on_plot_button)

        self.about_action = QAction("About SRT", self)
        self.about_action.triggered.connect(self.on_about_action)

    def create_menu(self):
        """Create the application"s menu bar."""
        self.menuBar().setNativeMenuBar(False)

        # Create File menu and add actions
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.new_window_action)
        file_menu.addAction(self.new_tab_action)
        file_menu.addSeparator()
        file_menu.addAction(self.import_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

        analysis_menu = self.menuBar().addMenu("Analysis")
        analysis_menu.addAction(self.describe_action)
        analysis_menu.addAction(self.info_action)
        analysis_menu.addAction(self.plot_action)

        about_menu = self.menuBar().addMenu("About")
        about_menu.addAction(self.about_action)

    def create_dock_widgets(self):
        self.right_dock = QDockWidget('Plots', self)
        self.left_dock = QDockWidget('Controls', self)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.right_dock)
        
    def create_toolbar(self):
        """Set up the navigation toolbar."""
        self.tool_bar = QToolBar("Address Bar")
        self.tool_bar.setIconSize(QSize(30, 30))
        self.addToolBar(self.tool_bar)
        
        # Create toolbar actions
        database_button = QAction(
            QIcon(Paths.icon("database.svg")), 
            "Database", 
            self
        )
        database_button.triggered.connect(self.on_database_button)

        reports_button = QAction(
            QIcon(Paths.icon("clipboard.svg")), 
            "Reports", 
            self
        )
        reports_button.triggered.connect(self.on_reports_button)

        sign_out_button = QAction(
            QIcon(Paths.icon("log-out.svg")), 
            "Sign Out", 
            self
        )
        sign_out_button.triggered.connect(self.on_sign_out_button)

        home_button = QAction(
            QIcon(Paths.icon("home.svg")), 
            "Home", 
            self
        )
        home_button.triggered.connect(self.on_home_button)

        logo = QAction(
            QIcon(Paths.image("StaySmartLogo1.png")),
            "Logo",
            self
        )

        file_button = QAction(
            QIcon(Paths.icon("file.svg")),
            "File",
            self
        )
        file_button.triggered.connect(self.on_import)

        profile_button = QAction(
            QIcon(Paths.icon("user.svg")), 
            "User", 
            self
        )
        profile_button.triggered.connect(self.on_profile_button)

        self.settings_button = QAction(
            QIcon(Paths.icon("settings.svg")),
            "Settings",
            self
        )
        self.settings_button.triggered.connect(self.on_settings_button)

        self.right_dock_toggle = QAction(
            QIcon(Paths.icon("trending-up.svg")),
            'Toggle Plot Dock',
            self
        )
        self.right_dock_toggle.triggered.connect(self.on_right_dock_toggle)

        self.left_dock_toggle = QAction(
            QIcon(Paths.icon('edit-3.svg')),
            'Toggle Control Dock',
            self
        )
        self.left_dock_toggle.triggered.connect(self.on_left_dock_toggle)

        self.tool_bar.addAction(logo)

        self.tool_bar.addSeparator()

        self.tool_bar.addAction(home_button)
        self.tool_bar.addAction(file_button)
        self.tool_bar.addAction(database_button)
        self.tool_bar.addAction(reports_button)

        self.tool_bar.addSeparator()

        self.tool_bar.addAction(self.left_dock_toggle)
        self.tool_bar.addAction(self.right_dock_toggle)

        self.tool_bar.addSeparator()

        self.tool_bar.addAction(profile_button)
        self.tool_bar.addAction(self.settings_button)
        self.tool_bar.addAction(sign_out_button) 

    def on_new_window(self):
        """Create new instance of the Browser class."""
        new_window = MainWindow()
        new_window.show()
        self.window_list.append(new_window)

    def on_new_tab(self):
        """Create a new web tab."""
        new_tab = QWidget()
        self.tab_bar.addTab(new_tab, "New Tab")

        # Update the tab_bar index to keep track of the new tab.
        # Load the url for the new page.
        tab_index = self.tab_bar.currentIndex()
        self.tab_bar.setCurrentIndex(tab_index + 1)

    def on_import(self):
        """Import file."""
        options = QFileDialog.Option.ReadOnly  # Optional: Set additional options as needed

        # Set filters for Markdown and PDF files
        filters = "CSV Files (*.csv);;Markdown Files (*.md);;PDF Files (*.pdf);;All Files (*)"

        # Show the file dialog for selecting files
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter(filters)
        file_paths, _ = file_dialog.getOpenFileNames(self, "Import Dataset", "", filters, options=options)

        # Handle the selected files
        self.handle_files(file_paths)

    def handle_files(self, file_paths):
        """Handle selected files."""
        for file_path in file_paths:
            if file_path.endswith('.md'):
                # Handle Markdown file
                self.handle_markdown(file_path)
            elif file_path.endswith('.pdf'):
                # Handle PDF file
                self.handle_pdf(file_path)
            elif file_path.endswith('.csv'):
                # Handle CSV file
                self.handle_csv(file_path)
            else:
                # Handle other file types
                self.handle_other(file_path)

    def handle_markdown(self, file_path):
        """
        Handle Markdown
        Disable the correct docks
        """
        print(f"Handling Markdown file: {file_path}")

        html_model = MarkdownModel(file_path)
        html_view = HtmlView(html_model.html_content)
        html_tree_view = TreeWidgetFactory().build_html_tree(self.left_dock, html_model.headers())

        self.tab_bar.addTab(html_view, html_model.title)
        tab_idx = self.tab_bar.count() - 1
        self.controllers[tab_idx] = html_tree_view
        
    def handle_pdf(self, file_path):
        # Code to handle PDF file
        print(f"Handling PDF file: {file_path}")

    def handle_other(self, file_path):
        """Handle other file types."""
        # Code to handle other file types
        print(f"File type, {file_path} is not supported.")

    def handle_csv(self, file_path):
        """
        Handle the CSV file from import. 
        Create a DataFrame to hold the data.
        Create a model to pass to QTableWidget.
        """
        print("Handling files...")

        # get the delimiter
        seperator = detect_csv_separator(file_path)
        df = read_csv(file_path, sep=seperator)

        # replace headers with human readable headers
        new = {old: Transformer.headers(old) for old in df.columns}
        df.rename(columns=new, inplace=True)

        # get title
        title = path_to_title(file_path)
        # set title to df
        df.attrs['title'] = title

        # create table view
        self.model = TableModel(df)
        table_widget = TableView(self.tab_bar, self.model)

        print("Control back to browser")
        self.tab_bar.addTab(table_widget, title)

        plotView = PlotView(self.right_dock)
        
        tab_idx = self.tab_bar.count() - 1

        # Add controller to list of controllers
        controller = ControlDockTabWidget(self.left_dock, df, table_widget, plotView)
        controller.sort_selection.connect(self.on_sort_selection)
        controller.visualizations_tab.plot_clicked.connect(self.on_plot_button)

        self.controllers[tab_idx] = controller

        # Add plotView to list of plotViews
        self.plot_views[tab_idx] = plotView
        return

    def updateProgressBar(self, progress):
        """Update progress bar in status bar.
        This provides feedback to the user that page is 
        still loading."""
        if progress < 100:
            self.page_load_pb.setVisible(progress)
            self.page_load_pb.setValue(progress)
            self.page_load_label.setVisible(progress)
            self.page_load_label.setText(f"Loading Page... ({str(progress)}/100)")
            self.status_bar.addWidget(self.page_load_pb)
            self.status_bar.addWidget(self.page_load_label)
        else:
            self.status_bar.removeWidget(self.page_load_pb)
            self.status_bar.removeWidget(self.page_load_label)

    def updateTabTitle(self):
        """Update the title of the tab to reflect the 
        file name."""
        tab_index = self.tab_bar.currentIndex()
        title = self.list_of_data_pages[self.tab_bar.currentIndex()].page().title()
        self.tab_bar.setTabText(tab_index, title)

    @pyqtSlot()
    def on_about_action(self):
        view = self.handle_markdown('About.md')
        # self.tab_bar.addTab(view, 'About')

    @pyqtSlot()
    def on_settings_button(self):
        if hasattr(self, 'user') and isinstance(self.user, User):
            # Check if there's already a settings tab and switch to it
            for i in range(self.tab_bar.count()):
                if isinstance(self.tab_bar.widget(i), SettingsView):
                    self.tab_bar.setCurrentIndex(i)
                    return

            # If not found, create a new settings tab
            settingsWidget = SettingsView(parent=self, main=self)
            tabIndex = self.tab_bar.addTab(settingsWidget, "Settings")
            self.tab_bar.setCurrentIndex(tabIndex)
        else:
            print("User object is not defined or not an instance of User.")



    @pyqtSlot()
    def on_database_button(self):
        print("Handle database button")
        return

    @pyqtSlot()
    def on_reports_button(self):
        # Open Reports Pane with 
        # Left Dock -> ModelingController
        controller = ModellingController(self.left_dock, self.model.cur_data)
        # Right Dock -> QTreeWidget
        # model_info = TreeWidgetFactory().build_classifier_tree(self.right_dock)

        # tab_widget -> PlotView()
        plotView = PlotView(self.tab_bar)
        self.tab_bar.addTab(plotView, "Prediction Report")
        self.tab_bar.setCurrentWidget(plotView)
        self.left_dock.setWidget(controller)
        return

    @pyqtSlot()
    def on_sign_out_button(self):
        print("Handle log-out button")

    @pyqtSlot()
    def on_home_button(self):
        print("Home Button")

    @pyqtSlot()
    def on_profile_button(self):
        if hasattr(self, 'user') and isinstance(self.user, User):
            # Check if there's already a profile tab and switch to it
            found = False
            for i in range(self.tab_bar.count()):
                if self.tab_bar.tabText(i) == "Profile":
                    self.tab_bar.setCurrentIndex(i)
                    found = True
                    break

            # If not found, create a new profile tab
            if not found:
                profileWidget = ProfileView(user=self.user, parent=self)
                tabIndex = self.tab_bar.addTab(profileWidget, "Profile")
                self.tab_bar.setCurrentIndex(tabIndex)
        else:
            print("User object is not defined or not an instance of User.")

    @pyqtSlot(int)
    def on_close_tab(self, tab_index):
        """Slot is emitted when the close button on a tab is clicked. 
        index refers to the tab that should be removed."""
        self.tab_bar.removeTab(tab_index)

    @pyqtSlot()
    def on_describe_action(self):
        pass

    @pyqtSlot()
    def on_info_action(self):
        pass

    @pyqtSlot()
    def on_plot_button(self):
        """
        Show the plot view when the plot button is clicked
        """
        if not self.right_dock.isVisible():
            self.right_dock.setVisible(True)
    
    @pyqtSlot()
    def on_right_dock_toggle(self):
        if self.right_dock.isVisible():
            self.right_dock.setVisible(False)
        else:
            self.right_dock.setVisible(True)

    @pyqtSlot()
    def on_left_dock_toggle(self):
        if self.left_dock.isVisible():
            self.left_dock.setVisible(False)
        else:
            self.left_dock.setVisible(True)

    @pyqtSlot(int)
    def on_tab_switch(self, tab_index):
        current_tab = self.tab_bar.widget(tab_index)
        if current_tab.type == 'TableView':
            # Show controller dock until a plot is plotted.
            self.right_dock.setVisible(False)
            self.right_dock_toggle.setEnabled(True)
            # Correlate the TableView with the correct PlotView
            self.right_dock.setWidget(self.plot_views[tab_index])
            # And with the correct controller.
            self.left_dock.setWidget(self.controllers[tab_index])

        elif current_tab.type == 'HtmlView':
            # Hide right dock
            self.right_dock.setVisible(False)
            self.right_dock_toggle.setEnabled(False)
            # Show left dock with proper widget
            self.left_dock.setVisible(True)
            self.left_dock_toggle.setEnabled(True)
            self.left_dock.setWidget(self.controllers[tab_index])

        else:
            # Hide Both
            self.right_dock.setVisible(False)
            self.right_dock.setEnabled(False)
            self.left_dock.setVisible(False)
            self.left_dock.setEnabled(False)

    @pyqtSlot(int)
    def on_sort_selection(self, col_idx):
        curr_table = self.tab_bar.currentWidget()
        curr_table.selectColumn(col_idx)
        return
        
    def sizeMainWindow(self):
        """Use QApplication.primaryScreen() to access information 
        about the screen and use it to size the application window 
        when starting a new application."""
        desktop = QApplication.primaryScreen()
        size = desktop.availableGeometry()
        screen_width = size.width() 
        screen_height = size.height() 
        self.setGeometry(0, 0, screen_width, screen_height)

    def closeEvent(self, arg_1):
        self.browser_closed.emit()
        return
    




# Widget for viewing markdown 
class HtmlView(QWidget):
    def __init__(self, html_content):
        super().__init__()
        self.type = 'HtmlView'
        self.html_content = html_content
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.text_browser = QTextBrowser()
        self.layout.addWidget(self.text_browser)
        self.text_browser.setHtml(self.html_content)
        self.setLayout(self.layout)

class ProfileView(QWidget):
    def __init__(self, user: User, parent=None):
        super().__init__(parent)
        self.type = "ProfileView"
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.user = user
        self.populate_user_data()

        # Hide the QLabel and replace it with QLineEdit for phone number input
        #self.replace_phone_number_label_with_input()

        self.ui.addPic_button.clicked.connect(self.add_pic)
        self.ui.changePass_button.clicked.connect(self.change_pass_window)
        #self.ui.addcontact_button.clicked.connect(self.addContactRow)
        #self.ui.delcontact_button.clicked.connect(self.delContactRow)
        #self.ui.contactInfo_button.clicked.connect(self.show_contactInfo)

    def populate_user_data(self):
        """Populate the UI with data from the User object."""
        self.ui.role.setText(self.user.get_role())
        self.ui.email.setText(self.user.get_email())
        self.ui.full_name.setText(self.user.get_name())
        # Assuming you have a method to get the phone number
        #self.ui.phoneNumberLabel.setText(self.user.get_phone_number())
    
    def add_pic(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (.png.xpm .jpg.bmp)")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            pixmap = QPixmap(file_path)

            if not pixmap.isNull():
                targetSize = self.ui.profile_pic.size()  # Ensure this is the correct reference to your QLabel
                scaledPixmap = pixmap.scaled(targetSize.width(), targetSize.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.ui.profile_pic.setPixmap(scaledPixmap)  # Ensure this is the correct reference to your QLabel
            else:
                QMessageBox.warning(self, "Image Load Error", "The selected image could not be loaded. Please try a different file.")

    def change_pass_window(self):
        print('Change Password')

class PlotView(QWidget):
    """
    Plot View Controlled by a PlotViewController
    View for Plotter, calls a model to render the plot.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

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

class Change_Pass_Window(QWidget):
    print('Password Changed')