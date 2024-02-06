# DataAnalysisPage is the view that is under the Data Analysis tab
# This view should control and maintain all interactions within the Data Analysis Tab

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, QMimeData
from tests.DataTable import DataWindow
from pandas import read_csv
import os

class DataAnalysisPage(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Home Page")

        # Create a central widget for the QMainWindow
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        

        # Create a layout for the central widget
        self.layout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.tab_widget = QtWidgets.QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # Set properties for drop events
        self.setAcceptDrops(True)

        # Create a QToolBar
        self.toolbar = QtWidgets.QToolBar("File Operations", self)
        self.addToolBar(self.toolbar)

        # Create actions for the toolbar
        self.import_action = QtGui.QAction("Import", self)
        self.import_action.setStatusTip("Import data set")
        self.import_action.triggered.connect(self.on_import_action)
        self.toolbar.addAction(self.import_action)

        self.save_action = QtGui.QAction("Save", self)
        self.save_action.setStatusTip("Save current tab")
        self.save_action.triggered.connect(self.on_save_action)
        self.toolbar.addAction(self.save_action)

        self.close_action = QtGui.QAction("Close", self)
        self.close_action.setStatusTip("Close current tab")
        self.close_action.triggered.connect(self.on_close_tab)
        self.toolbar.addAction(self.close_action)

        self.toolbar.addSeparator()

        self.plot_action = QtGui.QAction("Plot", self)
        self.plot_action.setStatusTip("Create a simple Plot")
        self.plot_action.triggered.connect(self.on_plot_action)
        self.toolbar.addAction(self.plot_action)

        self.info_action = QtGui.QAction("Info", self)
        self.info_action.setStatusTip("Show detailed info")
        self.info_action.triggered.connect(self.on_info_action)
        self.toolbar.addAction(self.info_action)

        self.describe_action = QtGui.QAction("Describe", self)
        self.describe_action.setStatusTip("Show table stats")
        self.describe_action.triggered.connect(self.on_describe_action)
        self.toolbar.addAction(self.describe_action)

        self.setStatusBar(QtWidgets.QStatusBar(self))
        

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()

        # Check if the MIME data contains URLs
        if mime_data.hasUrls():

            # Check each URL to see if it represents a CSV file
            for url in mime_data.urls():
                if url.isLocalFile() and url.toLocalFile().lower().endswith('.csv'):
                    # If at least one file is a CSV, accept the drop
                    event.acceptProposedAction()
                    return

        # If no CSV file is found, reject the drop event
        event.ignore()

    def on_plot_action(self):
        # Dialog to generate plot using the existing dataset
        return
    
    def on_import_action(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly  # Optional: Set additional options as needed

        # Show the file dialog for selecting CSV files
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        file_paths, _ = file_dialog.getOpenFileNames(self, "Import CSV Dataset", "", "CSV Files (*.csv);;All Files (*)", options=options)

        self.handle_files(file_paths)
        return

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            file_paths = [url.toLocalFile() for url in mime_data.urls()]
            self.handle_files(file_paths)

    def handle_files(self, file_paths):
        # Create dataframe array to hold file paths
        dataframes = []
        
        for path in file_paths:
            # Create df object from file paths
            df = read_csv(path)
            dataframes.append(df)
            data_table = DataWindow(df=df)
            self.tab_widget.addTab(data_table, os.path.basename(path))
            data_table.show()
        
        return
    
    def add_tab(self, widget, file_path):
        # Create a new QWidget for the tab
        w = QtWidgets.QWidget()

        # Customize the content of the tab
        label = QtWidgets.QLabel(file_path)
        layout = QtWidgets.QVBoxLayout(w)
        layout.addWidget(label)
        layout.addWidget(widget)

        # Add the new tab to the QTabWidget
        self.tab_widget.addTab(w, os.path.basename(file_path))


    def on_close_tab(self):
        # Logic to close the current tab
        current_tab_index = self.tab_widget.currentIndex()
        self.tab_widget.removeTab(current_tab_index)
    
    def on_save_action(self):
        # Logic to save data from the current tab
        current_tab_index = self.tab_widget.currentIndex()
        current_tab_name = self.tab_widget.tabText(current_tab_index)
        
        # Example: Show a file dialog for saving
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setWindowTitle(f"Save Data from {current_tab_name}")
        file_path, _ = file_dialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)")

        if file_path:
            # Get the Dataframe
            # Convert the Dataframe to csv
            # Move the csv to the file_path
            print(f"Save data from {current_tab_name} to: {file_path}")
        
    def on_info_action(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            df = current_tab.df
            print(df.info())
        else:
            print("No Tab to get info.")
        return

    def on_describe_action(self):
        # TODO: Need a way to close it
        # if checked, delete the description widget and title
        # if not checked, then show description for the current widget.
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            if self.describe_action.isChecked():
                self.layout.removeWidget()
            else:
                df = current_tab.df
                describe_window = DataWindow(df.describe())
                self.layout.addWidget(QtWidgets.QLabel("Description"))
                self.layout.addWidget(describe_window)
        else:
            print("No Tab to get describe.")
        return
