# This Python file uses the following encoding: utf-8

import os, os.path
import pandas as pd
from model.farm_model import (Farm, Group, Supply)

class Config:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new Config instance')
            cls._instance = cls.__new__(cls)
            cls._instance.new_instance()

        return cls._instance

    def new_instance(self):
        self.farm_empty = True

        self.folder_path = os.path.join(os.getcwd(), "data")
        self.settings_file = os.path.join(self.folder_path, "__settings.xml")
        self.group_file = os.path.join(self.folder_path, "__groups.csv")
        self.supply_file = os.path.join(self.folder_path, "__supplies.csv")
        self.animal_file = os.path.join(self.folder_path, "__animals.csv")
        self.expense_file = os.path.join(self.folder_path, "__expenses.csv")
        self.schedule_file = os.path.join(self.folder_path, "__schedules.csv")

        try:
            self.settings_df=pd.read_xml(self.settings_file)
            self.farm_empty = False
        except:
            self.farm_empty = True

    def empty(self):
        if self._instance is None:
            return True
        else:
            return self.farm_empty

    def config_new_farm(self, name):
        # Create a Settings file, with name, dir, and groups and supplies files
        data = [[name, self.folder_path, '__groups.csv','__supplies.csv']]
        df = pd.DataFrame(data,columns=['farm_name','wk_dir','groups_file','supplies_file'])
        df.to_xml(self.settings_file)

        # Create Groups file
        df = pd.DataFrame([], columns=['name'])
        df.to_csv(self.group_file)

        # Create Supplies file
        df = pd.DataFrame([], columns=['name','purchase_qty','units','price','notes','serving_qty'])
        df.to_csv(self.supply_file)

        # Create Animals file
        df = pd.DataFrame([], columns=['name','group','date_added','date_removed'])
        df.to_csv(self.animal_file)

        # Create Expenses file
        df = pd.DataFrame([], columns=['name','cost','group','animal','supply'])
        df.to_csv(self.expense_file)

        # Create Schedules file
        df = pd.DataFrame([], columns=['name','animal','supply','qty','day_time'])
        df.to_csv(self.schedule_file)

    def load(self):
        # Load Settings
        if(self.farm_empty):
            try:
                self.settings_df=pd.read_xml(self.settings_file)
                self.farm_empty = False
            except:
                raise Exception("File error: Not able to read settings file")

        name = self.settings_df.at[0,'farm_name']
        self.group_file = os.path.join(self.folder_path, self.settings_df.at[0,'groups_file'])
        self.supply_file = os.path.join(self.folder_path, self.settings_df.at[0,'supplies_file'])

        # Loads 5 tables
        try:
            self.groups_df=pd.read_csv(self.group_file)
            self.supplies_df=pd.read_csv(self.supply_file)
            self.animal_df=pd.read_csv(self.animal_file)
            self.expense_df=pd.read_csv(self.expense_file)
            self.schedule_df=pd.read_csv(self.schedule_file)
        except:
            raise Exception("File error: Not able to read group, supply, animal, expense, or schedule file(s)")

        Farm.create_farm(name, self.groups_df, self.supplies_df, self.animal_df, self.expense_df, self.schedule_df)



