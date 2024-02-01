from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, QMimeData
from tests.basic_table import DataWindow
from pandas import read_csv

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
        close_action = QtGui.QAction("Close", self)
        close_action.triggered.connect(self.close_tab)
        toolbar.addAction(close_action)

        save_action = QtGui.QAction("Save", self)
        save_action.triggered.connect(self.save_data)
        toolbar.addAction(save_action)

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


    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            file_paths = [url.toLocalFile() for url in mime_data.urls()]
            self.handle_dropped_files(file_paths)

    def handle_dropped_files(self, file_paths):
        # Create dataframe array to hold file paths
        dataframes = []
        
        for path in file_paths:
            # Create df object from file paths
            df = read_csv(path)
            dataframes.append(df)
        
        data_table = DataWindow(df=dataframes[0])
        self.add_tab(data_table)
        data_table.show()
        return
    
    def add_tab(self, widget):
        # Create a new QWidget for the tab
        w = QtWidgets.QWidget()

        # Customize the content of the tab
        label = QtWidgets.QLabel(f"Data Table View")
        layout = QtWidgets.QVBoxLayout(w)
        layout.addWidget(label)
        layout.addWidget(widget)

        # Add the new tab to the QTabWidget
        self.tab_widget.addTab(w, f"Data")

    def close_tab(self):
        # Logic to close the current tab
        current_tab_index = self.tab_widget.currentIndex()
        self.tab_widget.removeTab(current_tab_index)
    
    def save_data(self):
        # Logic to save data from the current tab
        current_tab_index = self.centralWidget().layout().itemAt(0).currentIndex()
        current_tab_name = self.centralWidget().layout().itemAt(0).tabText(current_tab_index)
        
        # Example: Show a file dialog for saving
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setWindowTitle(f"Save Data from {current_tab_name}")
        file_path, _ = file_dialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)")

        if file_path:
            # Implement saving logic here
            print(f"Save data from {current_tab_name} to: {file_path}")