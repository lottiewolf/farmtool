# This Python file uses the following encoding: utf-8

import os, os.path
import pandas as pd

class ConfigFarm:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new configuration...')
            cls._instance = cls.__new__(cls)
            cls._instance.init_settings()

        return cls._instance

    def init_settings(self):
        self.is_loaded = False
        self.not_named = True
        self.farmtool_path = os.path.join(os.getcwd(), "farm_tool")
        self.config_path = os.path.join(self.farmtool_path, "config")
        self.model_path = os.path.join(self.farmtool_path, "model")
        self.settings_file = os.path.join(self.config_path, "__settings.xml")
        self.name = ""
        self.db_path = os.path.join(self.model_path, "farmtool.db")
        self.version = "0.1"

    def load(self):
        # Load Settings File
        try:
            self.settings_df = pd.read_xml(self.settings_file)
            self.name = self.settings_df.at[0,'farm_name']
            self.db_path = self.settings_df.at[0,'db_path']
            self.version = self.settings_df.at[0,'version_num']
            self.is_loaded = True
            self.not_named = False
        except:
            print("Settings prepped, farm not yet named. Settings file not yet created.")

    def save_settings(self):
        data = [[self.name, self.db_path, self.version]]
        self.settings_df = pd.DataFrame(data,columns=['farm_name','db_path','version_num'])
        self.settings_df.to_xml(self.settings_file)
        print("Settings saved.")

    def set_name(self, name):
        self.name = name
        self.save_settings()
        self.not_named = False

    def get_name(self):
        return self.name

    def get_version(self):
        return self.version

    def get_db_path(self):
        return self.db_path

    def is_not_named(self):
        return self.not_named





