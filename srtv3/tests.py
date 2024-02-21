import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from bs4 import BeautifulSoup


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HTML Navigation")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create navigation tree widget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("Navigation")
        self.tree_widget.itemClicked.connect(self.on_tree_item_clicked)
        self.layout.addWidget(self.tree_widget)

        # Create web engine view
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)

        # Load HTML content
        with open("Welcome2.0.html", "r") as file:
            html_content = file.read()
        self.web_view.setHtml(html_content)

        # Parse HTML content to populate navigation tree
        self.populate_navigation_tree(html_content)

    def populate_navigation_tree(self, html_content):
        # Parse HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all headers (h1, h2, h3, etc.)
        headers = soup.find_all(["h1", "h2", "h3"])

        stack = []
        top_level = None

        for header in headers:
            # Get the tag name and text content of the header
            tag = header.name
            text = header.text.strip()
            
            # Check if the stack is empty or the tag name is greater than or equal to the top of the stack
            if not stack or tag >= stack[-1][0]:
                stack.append([tag, text])
                if top_level:
                    item = QTreeWidgetItem(top_level)
                else:
                    item = QTreeWidgetItem(self.tree_widget)
                item.setText(0, text)

                if tag == 'h2':
                    top_level = item
                    
            else:
                while stack and tag < stack[-1][0]:
                    stack.pop()
                    top_level = top_level.parent() if top_level else None
                # Push the tag name and the text content as a list to the stack
                stack.append([tag, text])
                # If there's a parent, set it as the current item
                if top_level:
                    item = QTreeWidgetItem(top_level)
                else:
                    item = QTreeWidgetItem(self.tree_widget)
                item.setText(0, text)
                # If the tag is h2, update the parent
                if tag == 'h2':
                    top_level = item

    def process_subheaders(self, parent_header, parent_item):
        # Find subheaders of the parent header
        subheaders = parent_header.find_next_siblings(["h1", "h2", "h3", "h4", "h5", "h6"])

        for subheader in subheaders:
            # Create a QTreeWidgetItem for the subheader
            subheader_item = QTreeWidgetItem([subheader.text.strip()])

            # Add subheader item to parent item
            parent_item.addChild(subheader_item)

            # Recursively process subheaders
            self.process_subheaders(subheader, subheader_item)

    def on_tree_item_clicked(self, item):
        print(f"Header: {item.text(0)} clicked")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
