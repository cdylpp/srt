from PySide6 import QtWidgets, QtCore
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
        tab_widget = QtWidgets.QTabWidget()
        layout.addWidget(tab_widget)

        # Create tabs for QTabWidget
        tab1 = QtWidgets.QWidget()
        tab2 = QtWidgets.QWidget()
        tab_widget.addTab(tab1, "Tab 1")
        tab_widget.addTab(tab2, "Tab 2")

        # Create the label
        label = QtWidgets.QLabel("Drop files here")
        layout.addWidget(label)

        # Set properties for drop events
        self.setAcceptDrops(True)


        # Create a QToolBar
        toolbar = QtWidgets.QToolBar("File Operations", self)
        self.addToolBar(toolbar)

        # Create actions for the toolbar
        close_action = QtWidgets.QAction("Close", self)
        close_action.triggered.connect(self.close_tab)
        toolbar.addAction(close_action)

        save_action = QtWidgets.QAction("Save", self)
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
        # Implement your logic to handle the dropped files
        # For example, display the file paths in the QLabel
        dataframes = []
        for path in file_paths:
            df = read_csv(path)
            dataframes.append(df)
        
        data_table = DataWindow(df=dataframes[0])
        self.centralWidget().layout().addWidget(data_table)
        data_table.show()
        return