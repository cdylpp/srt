# DataAnalysisPage is the view that is under the Data Analysis tab
# This view should control and maintain all interactions within the Data Analysis Tab
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, 
    QToolBar, QStatusBar, QVBoxLayout, QFileDialog, QWidget, 
    QVBoxLayout, QTextBrowser, QDockWidget,
    QMessageBox)

from PyQt6.QtCore import QSize, pyqtSignal, Qt, pyqtSlot
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter, QPainterPath, QBitmap, QColor, QPainter, QBrush
from PyQt6.QtWebEngineWidgets import QWebEngineView

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from widgets import (
    TreeWidgetFactory, TableView, 
    ControlDockTabWidget, ModellingController, MetricController)

from user import User
from models import TableModel, MarkdownModel, Classifier
from paths import Paths
from pandas import read_csv
import pyqtgraph as pg
from utils import detect_csv_separator, path_to_title, Transformer
from ProfileWindow import Ui_Form
from settings import SettingsView
from collections import namedtuple


style_sheet = """
    QTabWidget:pane{
        border: none
    }
"""

class MainWindow(QMainWindow):

    browser_closed = pyqtSignal()
    sign_out = pyqtSignal()

    def __init__(self, user_manager=None, app_data_manager=None): #replaced app_data=None
        super().__init__()
        self.user_manager = None
        self.app_data_manager = app_data_manager #replaced self.app_data = app_data
        self.user = user_manager.get_user()
        self.curr_model = None
        self.tabs = {} # key: int, value: tuple. Holds the widgets for each tab index

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
        self.tab_bar.currentChanged.connect(self.on_tab_switch) # Switch Tab logic

        self.create_dock_widgets()

        # Create Welcome View
        self.main_tab = self.handle_html(Paths.data('Welcome2.0.html'))
        # self.tab_bar.addTab(self.main_tab, "Welcome")

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
        self.menuBar().setNativeMenuBar(True)

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
            QIcon(Paths.icon("trending-up.svg")), 
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
            QIcon(Paths.icon("bar-chart-2.svg")),
            'Toggle Plot Dock',
            self
        )
        self.right_dock_toggle.triggered.connect(self.on_right_dock_toggle)

        self.left_dock_toggle = QAction(
            QIcon(Paths.icon('sliders.svg')),
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
        """Create a new tab."""
        # Update the tab_bar index to keep track of the new tab.
        # Load the url for the new page.
        tab_index = self.tab_bar.currentIndex()
        self.tab_bar.setCurrentIndex(tab_index + 1)

    def build_tab(self, title: str, center, left=None, right=None, data=None):
        Tab = namedtuple("Tab", ['title','main','l_dock','r_dock','data'])
        # switch the tab to the new window.
        idx = self.tab_bar.count()
        # update the tabs dict
        self.tabs[idx] = Tab(title, center, left, right, data)
        # set the correct widgets for the current tab
        self.tab_bar.addTab(center, title)
        self.tab_bar.setCurrentIndex(idx)
        
        return

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
            elif file_path.endswith('.html'):
                self.handle_html(file_path)
            else:
                # Handle other file types
                self.handle_other(file_path)
    
    def handle_html(self, file_path):
        # Create a QWebEngineView widget
        web_view = QWebEngineView(self)
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Load the content of a local file
        web_view.setHtml(html_content)
        web_view.titleChanged.connect(self.update_tab_title)


        # Build Navigation Widget
        tree = TreeWidgetFactory().build_nav_tree(self.left_dock, html_content)
        tree.setHeaderLabel("Navigation")
        tree.itemClicked.connect(self.nav_item_clicked)
        
        self.build_tab(web_view.title(), web_view, left=tree, data=html_content)

    def handle_markdown(self, file_path):
        """
        Handle Markdown
        Disable the correct docks
        """
        print(f"Handling Markdown file: {file_path}")

        html_model = MarkdownModel(file_path)
        html_view = QWebEngineView()
        html_view.setHtml(html_model.html_content)

        html_tree_view = TreeWidgetFactory().build_nav_tree(self.left_dock, html_model.html_content)

        self.build_tab(html_view.title(), html_view, html_tree_view, data=html_model)
        
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

        # create center view
        model = TableModel(df)
        table_widget = TableView(self.tab_bar, model)

        # create right widget
        plotView = PlotView(self.right_dock)

        # create left widget
        controller = ControlDockTabWidget(self.left_dock, df, table_widget, plotView)
        controller.sort_selection.connect(self.on_sort_selection)
        controller.visualizations_tab.plot_clicked.connect(self.on_plot_button)

        self.build_tab(title, table_widget, controller, plotView, df)
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


    def on_about_action(self):
        self.handle_html(Paths.data('About.html'))


    def on_settings_button(self):
        if hasattr(self, 'user') and isinstance(self.user, User):
            for i in range(self.tab_bar.count()):
                if isinstance(self.tab_bar.widget(i), SettingsView):
                    self.tab_bar.setCurrentIndex(i)
                    return

            settingsWidget = SettingsView(user=self.user, app_data_manager=self.app_data_manager, parent=self.tab_bar) #new line
            self.build_tab("Settings", settingsWidget)
        else:
            print("User object is not defined or not an instance of User.")


    def on_database_button(self):
        print("Handle database button")
        return


    def on_reports_button(self):
        # Open Reports Pane with
        title = "Predictive Analysis"
        # model
        classifier = Classifier(self.curr_model)
        # model controller
        left_controller = ModellingController(self.left_dock, self.curr_model, classifier)
        # view
        centerView = PlotView(self.tab_bar)
        # view controller
        right_controller = MetricController(self.right_dock, classifier, centerView)
        classifier.modelsBuilt.connect(self.on_models_built)

        self.build_tab(title, centerView, left_controller, right_controller, data=self.curr_model)

        return


    def on_sign_out_button(self):
        print("Handle log-out button")
        reply = QMessageBox.question(self, 'Confirm Logout',
                                     "Are you sure you want to log out?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.sign_out.emit()  # Emit the sign-out signal
            self.close()  # Close the main window


    def on_home_button(self):
        # Take the User back to the welcome Tab
        # if the user has an open welcome tab, bring the user to this tab.
        # else if the user does not have a welcome tab make one.
        for i, tab in self.tabs.items():
            if isinstance(tab.main, QWebEngineView) and tab.main.title() == "Welcome":
                self.tab_bar.setCurrentIndex(i)
                return
        
        # No tab index found.
        self.handle_html(Paths.data('Welcome2.0.html'))



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


    def on_close_tab(self, tab_index):
        """Slot is emitted when the close button on a tab is clicked. 
        index refers to the tab that should be removed."""
        self.tab_bar.removeTab(tab_index)


    def on_describe_action(self):
        pass


    def on_info_action(self):
        pass


    def on_plot_button(self):
        """
        Show the plot view when the plot button is clicked
        """
        if not self.right_dock.isVisible():
            self.right_dock.setVisible(True)
    

    def on_right_dock_toggle(self):
        if self.right_dock.isVisible():
            self.right_dock.setVisible(False)
        else:
            self.right_dock.setVisible(True)


    def on_left_dock_toggle(self):
        if self.left_dock.isVisible():
            self.left_dock.setVisible(False)
        else:
            self.left_dock.setVisible(True)


    def on_tab_switch(self, tab_index):
        _, current_tab, left_widget, right_widget, data = self.tabs[tab_index]

        if isinstance(current_tab, (QWebEngineView, HtmlView)):
            # Hide right dock
            self.right_dock.setVisible(False)
            self.right_dock_toggle.setEnabled(False)
            # Show left dock with proper widget
            self.left_dock.setVisible(True)
            self.left_dock_toggle.setEnabled(True)
            self.left_dock.setWidget(left_widget)


        elif isinstance(current_tab, TableView):
            # Show controller dock until a plot is plotted.
            self.right_dock.setVisible(False)
            self.right_dock_toggle.setEnabled(True)
            # Correlate the TableView with the correct PlotView
            self.right_dock.setWidget(right_widget)
            # And with the correct controller.
            self.left_dock.setWidget(left_widget)


        elif isinstance(current_tab, PlotView):
            # Hide Right
            self.right_dock.setVisible(False)
            self.right_dock_toggle.setEnabled(False)
            # Show Left
            self.left_dock.setVisible(True)
            self.left_dock_toggle.setEnabled(True)
            self.left_dock.setWidget(left_widget)

        else:
            # Hide Both
            self.right_dock.setVisible(False)
            self.right_dock.setEnabled(False)
            self.left_dock.setVisible(False)
            self.left_dock.setEnabled(False)

            # Set both docks
            self.left_dock.setWidget(QWidget())
            self.right_dock.setWidget(QWidget())
        
        # set the current data
        self.curr_model = data
    

    def on_models_built(self):
        # Get the tree view from the right controller
        cur_idx = self.tab_bar.currentIndex()
        right_controller = self.tabs[cur_idx].r_dock
        self.right_dock.setWidget(right_controller.tree)

        # show the right dock
        self.right_dock.setVisible(True)
        self.right_dock_toggle.setEnabled(True)


    def on_sort_selection(self, col_idx):
        curr_table = self.tab_bar.currentWidget()
        curr_table.selectColumn(col_idx)
        return

    def nav_item_clicked(self, item):
        print(f"Header: {item.text(0)} clicked")

    def update_tab_title(self, title):
        cur_idx = self.tab_bar.currentIndex()
        self.tab_bar.setTabText(cur_idx, title)
        pass


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

    def scale_and_round_image(self, pixmap, targetSize):
        scaled_pixmap = pixmap.scaled(targetSize, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        rounded_pixmap = QPixmap(targetSize)
        rounded_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(scaled_pixmap))
        painter.setPen(Qt.GlobalColor.transparent)
        painter.drawRoundedRect(0, 0, targetSize.width(), targetSize.height(),targetSize.width() / 2, targetSize.height() / 2)
        painter.end()
        return rounded_pixmap

    def set_profile_picture(self, pixmap):
        self.ui.profile_pic.setMask(pixmap.mask())
        self.ui.profile_pic.setPixmap(pixmap)

    def populate_user_data(self):
        self.ui.role.setText(self.user.get_role())
        self.ui.email.setText(self.user.get_email())
        self.ui.full_name.setText(self.user.get_name())

        default_profile_pics = {
            "k.ross": "C:\\Users\\karen\\OneDrive\\Pictures\\app\\20231007_171153.copy13.jpg",
            "c.lepp": "path_to_default_image2.png",
            "a.carrigan": "path.png",
            "j.gilligan": "path.png",
            "a.mason": "path.png",
            "d.wood": "path.png",
        }

        default_pic_path = default_profile_pics.get(self.user.get_username(), None)
        if default_pic_path:
            self.user.set_profile_pic_path(default_pic_path)
            pixmap = QPixmap(default_pic_path)
        else:
            profile_pic_path = self.user.get_profile_pic_path()
            pixmap = QPixmap(profile_pic_path) if profile_pic_path else QPixmap("path_to_placeholder_image.png")

        scaled_rounded_pixmap = self.scale_and_round_image(pixmap, self.ui.profile_pic.size())
        self.set_profile_picture(scaled_rounded_pixmap)

    def add_pic(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            pixmap = QPixmap(file_path)

            if not pixmap.isNull():
                scaled_rounded_pixmap = self.scale_and_round_image(pixmap, self.ui.profile_pic.size())
                self.set_profile_picture(scaled_rounded_pixmap)
                self.user.set_profile_pic_path(file_path)
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

class Change_Pass_Window(QWidget):
    print('Password Changed')