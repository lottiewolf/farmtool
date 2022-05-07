# This Python file uses the following encoding: utf-8

from farm_tool.config.config_farm import ConfigFarm
import sys
import os
import pandas as pd


class Exporter:
    def __init__(self):
        self.settings_df = pd.read_csv("data/settings.csv")
        self.my_df = pd.read_csv("data/group_db.csv")

    def add_record(self, object):
        if type(object) is Animal:
            #append object to Animal file
            self.my_df.to_csv("data/group_db.csv")
            print(object)
        elif type(object) is Group:
            #append object to Group
            pass
        elif type(object) is Expense:
            #append to Expense
            pass
        elif type(object) is Schedule:
            #append Schedule
            pass
        elif type(object) is Supply:
            #append Supply
            pass
        else:
            raise Exception("Unknown object. Record not added to database")


#        self.folder_path = os.path.join(os.getcwd(), "data")
#        self.settings_file = os.path.join(self.folder_path, "__settings.xml")
#        self.gp_df=pd.read_csv(self.group_file)
# Create Groups file
# df = pd.DataFrame([], columns=['name'])
# df.to_csv(self.group_file)

# Loads 5 tables
# try:
#    self.groups_df=pd.read_csv(self.group_file)
#    self.supplies_df=pd.read_csv(self.supply_file)
#    self.animal_df=pd.read_csv(self.animal_file)
#    self.expense_df=pd.read_csv(self.expense_file)
#    self.schedule_df=pd.read_csv(self.schedule_file)
# except:
#    raise Exception("File error: Not able to read group, supply, animal, expense, or schedule file(s)")
# def refresh(self, flag):
#    try:
#        if flag == "groups":
#            self.df=pd.read_csv(self.group_file)
#        elif flag == "supplies":
#            self.df=pd.read_csv(self.supply_file)
#        elif flag == "animals":
#            self.df=pd.read_csv(self.animal_file)
#        elif flag == "expenses":
#            self.df=pd.read_csv(self.expense_file)
#        elif flag == "schedules":
#            self.df=pd.read_csv(self.schedule_file)
#        else:
#            raise Exception("No flag found")
#    except:
#        raise Exception("Could not read db")
#    return self.df
