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