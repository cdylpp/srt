from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, QMimeData
from tests.basic_table import DataWindow
from pandas import read_csv
import os

class HomePage(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Home Page")

        # Create a central widget for the QMainWindow
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Add a QTabWidget
        self.tab_widget = QtWidgets.QTabWidget()
        layout.addWidget(self.tab_widget)

        # Create the label
        label = QtWidgets.QLabel("Drop files here")
        layout.addWidget(label)

        # Set properties for drop events
        self.setAcceptDrops(True)

        # Create a QToolBar
        toolbar = QtWidgets.QToolBar("File Operations", self)
        self.addToolBar(toolbar)

        # Create actions for the toolbar
        import_action = QtGui.QAction("Import", self)
        import_action.setStatusTip("Import data set")
        import_action.triggered.connect(self.import_dataset_dialog)
        toolbar.addAction(import_action)

        save_action = QtGui.QAction("Save", self)
        save_action.setStatusTip("Save current tab")
        save_action.triggered.connect(self.save_data)
        toolbar.addAction(save_action)

        close_action = QtGui.QAction("Close", self)
        close_action.setStatusTip("Close current tab")
        close_action.triggered.connect(self.close_tab)
        toolbar.addAction(close_action)
        toolbar.addSeparator()

        create_plot = QtGui.QAction("Plot", self)
        create_plot.setStatusTip("Create a simple Plot")
        create_plot.triggered.connect(self.generate_plot_dialog)
        toolbar.addAction(create_plot)
        

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

    def generate_plot_dialog(self):
        # Dialog to generate plot using the existing dataset
        return
    
    def import_dataset_dialog(self):
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
            self.add_tab(data_table, path)
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

    def close_tab(self):
        # Logic to close the current tab
        current_tab_index = self.tab_widget.currentIndex()
        self.tab_widget.removeTab(current_tab_index)
    
    def save_data(self):
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