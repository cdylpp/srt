from PySide6 import QtWidgets, QtCore
from tests.AppDataManager import AppDataManager


class AccountUnlockDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Account Unlock")

        self.app_data_manager = AppDataManager()
        self.app_data = self.app_data_manager.get_app_data()

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        self.user_list = QtWidgets.QListWidget()
        self.user_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        # Populate user list with users having > 2 login attempts
        for user in self.app_data['login_attempts']:
            # TODO: Needs to check the number of login attempts
            item = QtWidgets.QListWidgetItem(user)
            self.user_list.addItem(item)

        layout.addWidget(QtWidgets.QLabel("Select users to reset login attempts:"))
        layout.addWidget(self.user_list)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def get_selected_users(self):
        selected_users = []
        for item in self.user_list.selectedItems():
            selected_users.append(item.text())
        return selected_users


class SettingsPage(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings Page")

        self.account_unlock_button = QtWidgets.QPushButton("Account Unlock")
        self.account_unlock_button.clicked.connect(self.show_account_unlock_dialog)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.account_unlock_button)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_account_unlock_dialog(self):
        dialog = AccountUnlockDialog(self)
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            selected_users = dialog.get_selected_users()
            self.reset_login_attempts(selected_users)

    def reset_login_attempts(self, users):
        app_data_manager = AppDataManager()
        users_data = app_data_manager.get_app_data()["users"]

        for user in users:
            if user in users_data:
                users_data[user]["login_attempts"] = 0

        app_data_manager.update_json()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    settings_page = SettingsPage()
    settings_page.show()
    app.exec()