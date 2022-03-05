# This Python file uses the following encoding: utf-8

import sys
import os
import pandas as pd

class Exporter:
    def __init__(self):
        settings_df = pd.read_csv("data/settings.csv")
        my_df = pd.read_csv("data/group_db.csv")

    def add_record(object):
        if object is Animal:
            #append object to Animal file
            my_df.to_csv("data/group_db.csv")
        elif object is Group:
            #append object to Group
            pass
        elif object is Expense:
            #append to Expense
            pass
        elif object is Schedule:
            #append Schedule
            pass
        elif object is Supply:
            #append Supply
            pass
        else:
            raise Exception("Unknown object. Record not added to database")

