# Starts on line 91 of LoginWindow

def valid_login(self, username, password):
    if self.login_attempts >= 3:
        self.disable_login()
        return False
    if self.db_manager.is_valid(username, password):
        return True
    else:
        self.login_attempts += 1
        return False


def on_rejection(self, username):
    self.app_data.log_login_attempts(username)
    self.user_manager.failed_attempt()

    if self.user_manager.get_login_attempts() >= 2:
        self.disable_login()
        QtWidgets.QMessageBox.warning(self, 'Account Locked',
                                      'Your account has been locked. Contact your system administrator.')
    else:
        QtWidgets.QMessageBox.warning(self, 'Login Failed', 'Invalid credentials.')


def disable_login(self):
    self.ui.password_input.setEnabled(False)
    self.ui.login_button.setEnabled(False)

# Next code is def increment_login_attempts