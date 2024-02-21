import os
import math
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QApplication, QScrollArea
from PyQt6.QtGui import QIcon
from paths import Paths

def list_files(directory):
    file_paths = []
    # Walk through all files and subdirectories in the given directory
    for root, directories, files in os.walk(directory):
        for file in files:
            # Join the directory path with the filename to create the full file path
            file_path = file
            # Append the file path to the list
            file_paths.append(file_path)
    return file_paths


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        scroll_area = QScrollArea()

        content = QWidget()
        content_layout = QVBoxLayout()
        icons = list_files('Icons')

        for icon in icons:
            h_layout = QHBoxLayout()
            label = QLabel(icon[:-4])
            img_label = QLabel()
            img = QIcon(Paths.icon(icon))
            pixmap = img.pixmap(30, 30)
            img_label.setPixmap(pixmap)
            h_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)
            h_layout.addWidget(img_label, alignment=Qt.AlignmentFlag.AlignRight)
            content_layout.addLayout(h_layout)
        
        
        content.setLayout(content_layout)
        scroll_area.setWidget(content)
        layout.addWidget(scroll_area)

        self.setLayout(layout)
    

app = QApplication([])
main = MainWindow()
main.show()
app.exec()
                

