# This Python file uses the following encoding: utf-8

import os, os.path
import pandas as pd
from model.farm_model import (Farm, Group, Supply)

class Config:
    def __init__(self):
        self.farm_empty = True

        self.folder_path = os.path.join(os.getcwd(), "data")
        self.settings_file = os.path.join(self.folder_path, "__settings.xml")
        try:
            self.settings_df=pd.read_xml(self.settings_file)
            self.farm_empty = False
        except:
            self.farm_empty = True

    def empty(self):
        return self.farm_empty

    def setup(self, name):
        data = [[name, self.folder_path, '__groups.csv','__supplies.csv']]
        df = pd.DataFrame(data,columns=['farm_name','wk_dir','groups_file','supplies_file'])
        df.to_xml(self.settings_file)

    def load(self):
        if(self.farm_empty):
            try:
                self.settings_df=pd.read_xml(self.settings_file)
                self.farm_empty = False
            except:
                raise Exception("File error")

        name = self.settings_df.at[0,'farm_name']
        self.group_file = os.path.join(self.folder_path, self.settings_df.at[0,'groups_file'])
        self.supply_file = os.path.join(self.folder_path, self.settings_df.at[0,'supplies_file'])
        try:
            self.groups_df=pd.read_csv(self.group_file)
        except:
            df = pd.DataFrame([], columns=['pk','name'])
            df.to_csv(self.group_file)
        try:
            self.supplies_df=pd.read_csv(self.supply_file)
        except:
            df = pd.DataFrame([], columns=['pk','name','purchase_qty','units','price','notes','serving_qty'])
            df.to_csv(self.supply_file)

        try:
            self.groups_df=pd.read_csv(self.group_file)
            self.supplies_df=pd.read_csv(self.supply_file)
        except:
            raise Exception("File error")

        return Farm(name, self.groups_df, self.supplies_df)

