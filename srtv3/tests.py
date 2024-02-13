from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from bs4 import BeautifulSoup



# Create an application instance
app = QtWidgets.QApplication(sys.argv)

# Create a main window
window = QtWidgets.QMainWindow()


# Sample HTML content
html_content = """
<h1>Welcome to Student Retention Analysis</h1>
<h2>Getting Started</h2>
<h3>Descriptive Statistics</h3>
<h3>Filtering and Sorting</h3>
<h2>Describe</h2>
<h2>Plot</h2>
<h3>Bar Chart</h3>
<h3>Pie Chart</h3>
<h2>Report</h2>
"""

# Initialize a QTreeWidget
tree = QtWidgets.QTreeWidget()
tree.setColumnCount(1)  # Set the number of columns

# Parse HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize a stack to keep track of hierarchy
stack = []

# Initialize a parent variable to keep track of the current parent
parent = None

# Iterate over headers
for header in soup.find_all(['h1', 'h2', 'h3']):
    # Get the tag name and text content of the header
    tag = header.name
    text = header.text.strip()
    
    # Check if the stack is empty or the tag name is greater than or equal to the top of the stack
    if not stack or tag >= stack[-1][0]:
        # Push the tag name and the text content as a list to the stack
        stack.append([tag, text])
        # If there's a parent, set it as the current item
        if parent:
            item = QtWidgets.QTreeWidgetItem(parent)
        else:
            item = QtWidgets.QTreeWidgetItem(tree)
        item.setText(0, text)
        # If the tag is h2, update the parent
        if tag == 'h2':
            parent = item
    else:
        # The tag name is smaller than the top of the stack
        # Pop the stack until the top is equal to or smaller than the tag name
        while stack and tag < stack[-1][0]:
            stack.pop()
            parent = parent.parent() if parent else None
        # Push the tag name and the text content as a list to the stack
        stack.append([tag, text])
        # If there's a parent, set it as the current item
        if parent:
            item = QtWidgets.QTreeWidgetItem(parent)
        else:
            item = QtWidgets.QTreeWidgetItem(tree)
        item.setText(0, text)
        # If the tag is h2, update the parent
        if tag == 'h2':
            parent = item

# Show the tree widget
tree.show()


# Add the QTreeWidget widget to the main window
window.setCentralWidget(tree)

# Show the main window
window.show()

# Start the application's main loop
sys.exit(app.exec())
