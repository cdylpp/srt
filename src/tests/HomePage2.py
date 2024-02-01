from PySide6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt

class HomePage(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Home Page")

        # Create a central widget for the QMainWindow
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Add a QTabWidget
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # Create tabs for QTabWidget
        tab1 = QWidget()
        tab2 = QWidget()
        tab_widget.addTab(tab1, "Tab 1")
        tab_widget.addTab(tab2, "Tab 2")

        # Set properties for drop events
        self.setAcceptDrops(True)

        # Create a QToolBar
        toolbar = QToolBar("File Operations", self)
        self.addToolBar(toolbar)

        # Create actions for the toolbar
        close_action = QAction("Close", self)
        close_action.triggered.connect(self.close_tab)
        toolbar.addAction(close_action)

        save_action = QAction("Save", self)
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

    def close_tab(self):
        # Implement logic to close the current tab
        current_tab_index = self.centralWidget().layout().itemAt(0).currentIndex()
        self.centralWidget().layout().itemAt(0).removeTab(current_tab_index)

    def save_data(self):
        # Implement logic to save data from the current tab
        current_tab_index = self.centralWidget().layout().itemAt(0).currentIndex()
        current_tab_name = self.centralWidget().layout().itemAt(0).tabText(current_tab_index)
        
        # Example: Show a file dialog for saving
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle(f"Save Data from {current_tab_name}")
        file_path, _ = file_dialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)")

        if file_path:
            # Implement saving logic here
            print(f"Save data from {current_tab_name} to: {file_path}")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    home_page = HomePage()
    home_page.show()
    sys.exit(app.exec())
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QTabWidget, QWidget, QToolBar, QAction, QFileDialog
from PyQt6.QtCore import Qt

class HomePage(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Home Page")

        # Create a central widget for the QMainWindow
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Add a QTabWidget
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # Create tabs for QTabWidget
        tab1 = QWidget()
        tab2 = QWidget()
        tab_widget.addTab(tab1, "Tab 1")
        tab_widget.addTab(tab2, "Tab 2")

        # Set properties for drop events
        self.setAcceptDrops(True)

        # Create a QToolBar
        toolbar = QToolBar("File Operations", self)
        self.addToolBar(toolbar)

        # Create actions for the toolbar
        close_action = QAction("Close", self)
        close_action.triggered.connect(self.close_tab)
        toolbar.addAction(close_action)

        save_action = QAction("Save", self)
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

    def close_tab(self):
        # Implement logic to close the current tab
        current_tab_index = self.centralWidget().layout().itemAt(0).currentIndex()
        self.centralWidget().layout().itemAt(0).removeTab(current_tab_index)

    def save_data(self):
        # Implement logic to save data from the current tab
        current_tab_index = self.centralWidget().layout().itemAt(0).currentIndex()
        current_tab_name = self.centralWidget().layout().itemAt(0).tabText(current_tab_index)
        
        # Example: Show a file dialog for saving
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle(f"Save Data from {current_tab_name}")
        file_path, _ = file_dialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)")

        if file_path:
            # Implement saving logic here
            print(f"Save data from {current_tab_name} to: {file_path}")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    home_page = HomePage()
    home_page.show()
    sys.exit(app.exec())
