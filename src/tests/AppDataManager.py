import os, sys
import json

#APP_DATA = os.path.abspath('data/app_data.json')   """references src\\data\\app_data.json instead of data\\app_data.json"""

"""Project Runs with added lines 8-17 """
# Get the directory of the current script (AppDataManager.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Move up to the parent directory (tests)
tests_dir = os.path.dirname(script_dir)

# Move up to the grandparent directory (SRTv.2)
parent_dir = os.path.dirname(tests_dir)

# Construct the absolute path to app_data.json in the data folder
APP_DATA = os.path.join(parent_dir, 'data', 'app_data.json')

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