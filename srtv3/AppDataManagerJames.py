import os, sys
import json

APP_DATA = os.path.relpath('data/app_data.json')


class AppDataManager:
    def __init__(self) -> None:
        self._data = self.get_app_data()
        pass

    def update_json(self):
        """
        Updates App Data
        """
        with open(APP_DATA, 'w') as jfile:
            json.dump(self._data, jfile, indent=4)

        return

    def clear_prev_user(self):
        """
        Removes previous user 
        """
        self._data['prev_user'] = ""
        self.update_json()
        return

    def get_prev_user(self) -> str:
        """
        Returns the username of the previous user. Set the previous user with `remember me` toggle button
        """
        with open(APP_DATA, 'r') as jfile:
            profile_data = json.load(jfile)

        return profile_data['prev_user']

    def get_app_data(self) -> dict:
        """
        Returns the App data as a dict.
        """
        with open(APP_DATA, 'r') as jfile:
            app_data = json.load(jfile)
        
        return app_data
    
    def save_user(self, username) -> None:
        # Save the username if the check box is checked.
        self._data['prev_user'] = username
        self.update_json()
        print("prev_user set to: ", username)
        return

    def get_login_attempts(self, username) -> int:
        return self._data.get(username, {}).get('login_attempts', 0)

    def set_login_attempts(self, username, attempts):
        if username not in self._data:
            self._data[username] = {}
        self._data[username]['login attempts'] = attempts
        self.update_json()

    def is_user_locked_out(self, username) -> bool:
        return self._data.get(username, {}).get('locked_out', False)

    def set_user_lockout(self, username, locked_out):
        if username not in self._data:
            self._data[username] = {}
        self._data[username]['locked_out'] = locked_out
        self.update_json()

    def get_locked_accounts(self):
        """Returns a list of usernames that are locked out."""
        locked_accounts = []
        for username, user_data in self._data.items():
            if user_data.get('locked_out', False):
                locked_accounts.append({'username': username})
        return locked_accounts

    def reset_account_lock(self, username):
        """Resets the lock status and login attempts for a given username."""
        if username in self._data:
            self._data[username]['locked_out'] = False
            self._data[username]['login_attempts'] = 0
            self.update_json()