# This Python file uses the following encoding: utf-8

#from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QApplication)
#from PySide6.QtWidgets import (QDockWidget, QListWidget, QMainWindow)
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

#from PySide6.QtCore import (QFile, Qt)
from model.farm_model import (Farm, Animal, Group, Expense, Schedule, Supply)
from model.data_model import PandasModel
from db.export import Exporter
#from ui.CreateFarmDialog import CreateFarmDialog
import os, os.path
import pandas as pd
import sys



class HelpWidget(QDockWidget):
    def __init__(self, main_window):
        QDockWidget.__init__(self, "Help Window", main_window)

        self.listWidget = QListWidget()
        self.listWidget.addItem("item1")
        self.listWidget.addItem("item2")
        self.listWidget.addItem("item3")
        self.setWidget(self.listWidget)
        self.setFloating(False)

        #dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        #dockWidget.setWidget(dockWidgetContents)
        #addDockWidget(Qt.LeftDockWidgetArea, dockWidget)

class MainWidget(QGroupBox):
    def __init__(self, main_window):
        QGroupBox.__init__(self, "  Farm Tool")

        farmview = QTableView()
        farmview.resize(500, 300)
        farmview.horizontalHeader().setStretchLastSection(True)
        farmview.setAlternatingRowColors(True)
        farmview.setSelectionBehavior(QTableView.SelectRows)
        print(main_window.get_farm())
        #model = PandasModel(main_window.get_farm().get_groups())
        #farmview.setModel(model)
        #self.layout = QFormLayout()
        #self.layout.addRow(farmview)
        #self.setLayout(self.layout)


class GroupWidget(QGroupBox):
    def __init__(self, main_window):
        QGroupBox.__init__(self, "  Add a Group")

        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Please enter group name below:", alignment=Qt.AlignCenter))
        #layout = QHBoxLayout()
        #outerLayout = QVBoxLayout()
        self.layout.addRow(QLabel("Name"), QLineEdit())
        self.setLayout(self.layout)

        #b2 = QPushButton(win)
        #b2.setText("Button2")
        #b2.move(50,50)
        #QObject.connect(b2,SIGNAL("clicked()"),b2_clicked) #b2clicked is a function defined below
        #horse = Animal("Penny", "Red Barn", 1, 2)
        #hay = Supply("hay", 10, "flakes", 10, "bale avg is 10", 2)
        #penny_sched = Schedule(horse, hay, 1)
        #tester = (horse.name + penny_sched.supply.name)
        #export = Exporter()
        #export.add_record(horse)


class ScheduleWidget(QGroupBox):
    def __init__(self, main_window):
        QGroupBox.__init__(self, "  Add a Schedule")

        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Please enter a daily schedule below:", alignment=Qt.AlignCenter))
        self.layout.addRow(QLabel("Name of Animal"), QLineEdit())
        self.layout.addRow(QLabel("Supply"), QComboBox())
        self.layout.addRow(QLabel("Date"), QSpinBox())
        self.setLayout(self.layout)


class ExpenseWidget(QGroupBox):
    def __init__(self, main_window):
        QGroupBox.__init__(self, "  Add an Expenses")

        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Please enter expense information below:", alignment=Qt.AlignCenter))
        self.layout.addRow(QLabel("Cost"), QLineEdit())
        self.layout.addRow(QLabel("Type"), QLineEdit())
        self.layout.addRow(QLabel("Date"), QLineEdit())
        #self.layout.addRow(QLabel("Degree"), QComboBox())
        #self.layout.addRow(QLabel("Age"), QSpinBox())
        self.setLayout(self.layout)
