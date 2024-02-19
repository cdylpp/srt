import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # The file URL
    file_url = QUrl('obsidian://open?vault=Obsidian%20Vault&file=Building%20Upon%20the%20Use%20Case')
    
    # Open the file URL
    QDesktopServices.openUrl(file_url)
    
    sys.exit(app.exec_())
