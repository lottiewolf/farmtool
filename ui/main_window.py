# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QTabWidget)
from PySide6.QtCore import Qt
from config.config_farm import ConfigFarm
from ui.main_menu import MainMenu
from ui.group_widget import GroupWidget
from ui.animal_widget import AnimalWidget
from ui.schedule_widget import ScheduleWidget
from ui.supply_widget import SupplyWidget
from ui.expense_widget import ExpenseWidget
from ui.help_widget import HelpWidget
from ui.create_farm_dialog import CreateFarmDialog
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        settings = ConfigFarm.instance()
        self.title_version = "Farm Tool " + str(settings.get_version())
        self.setWindowTitle(self.title_version)
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

        if(settings.is_not_named()):
            self.show()
            dlg = CreateFarmDialog()
            if dlg.exec():
                settings.set_name(dlg.textValue())
            else:
                sys.exit()

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

        self.setWindowTitle(self.title_version + "  -  " +
                            str(settings.get_name()) + " Overview")
        self.gp_tab.update_gp()
        self.anim_tab.update_anim()
        self.sched_tab.update_sched()
        self.supply_tab.update_supply()
        self.expense_tab.update_expense()
        self.tabs.setCurrentIndex(0)
        self.show()
