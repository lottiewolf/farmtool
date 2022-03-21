# This Python file uses the following encoding: utf-8

import sys
import os
import pandas as pd
from model.farm_model import (Animal, Group, Expense, Schedule, Supply)

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

