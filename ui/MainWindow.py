# This Python file uses the following encoding: utf-8

import sys
from PySide6.QtWidgets import (QMainWindow, QApplication, QFormLayout, QVBoxLayout, QTabBar, QTabWidget, QWidget)
from PySide6.QtCore import Qt
from ui.MainMenu import MainMenu
from ui.GroupWidget import GroupWidget
from ui.AnimalWidget import AnimalWidget
from ui.ScheduleWidget import ScheduleWidget
from ui.SupplyWidget import SupplyWidget
from ui.ExpenseWidget import ExpenseWidget
from ui.HelpWidget import HelpWidget
from ui.Config import Config
from model.farm_model import Farm
from ui.CreateFarmDialog import CreateFarmDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # for next version, put mainwindow in its own file
        self.version = "Farm Tool 0.1"
        self.setWindowTitle(self.version)
        self.menubar = MainMenu(self)
        self.statusBar()

        self.tabs = QTabWidget()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.tabs)
        self.setLayout(self.mainLayout)
        self.setCentralWidget(self.tabs)

        self.helpWidget = HelpWidget(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.helpWidget)
        self.resize(1000, 800)

        self.farm_config = Config.instance()
        if(self.farm_config.empty()):
            self.show()
            dlg = CreateFarmDialog()
            if dlg.exec():
                self.farm_config.config_new_farm(dlg.textValue())
            else:
                sys.exit()

        self.farm_config.load()

        self.gp_tab = GroupWidget()
        self.anim_tab = AnimalWidget()
        self.sched_tab = ScheduleWidget()
        self.supply_tab = SupplyWidget()
        self.expense_tab = ExpenseWidget()


        self.tabs.addTab(self.gp_tab, "Groups")
        self.tabs.addTab(self.anim_tab, "Animals")
        self.tabs.addTab(self.sched_tab, "Schedules")
        self.tabs.addTab(self.supply_tab, "Supplies")
        self.tabs.addTab(self.expense_tab, "Expenses")

        self.setWindowTitle(self.version + "  -  " + Farm.instance().get_name() + " Overview")
        self.gp_tab.update_gp()
        self.anim_tab.update_anim()
        self.sched_tab.update_sched()
        self.supply_tab.update_supply()
        self.expense_tab.update_expense()
        #self.tabs.insertTab(0, self.gp_tab, "Groups")
        self.tabs.setCurrentIndex(0)
        self.show()
