# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QTabWidget)
from PySide6.QtCore import Qt
from farm_tool.config.config_farm import ConfigFarm
from farm_tool.ui.main_menu import MainMenu
from farm_tool.ui.group_widget import GroupWidget
from farm_tool.ui.animal_widget import AnimalWidget
from farm_tool.ui.schedule_widget import ScheduleWidget
from farm_tool.ui.supply_widget import SupplyWidget
from farm_tool.ui.expense_widget import ExpenseWidget
from farm_tool.ui.help_widget import HelpWidget
from farm_tool.ui.create_farm_dialog import CreateFarmDialog
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.settings = ConfigFarm.instance()
        self.title_version = "Farm Tool " + str(self.settings.get_version())
        self.setWindowTitle(self.title_version)
        self.menubar = MainMenu(self)
        self.statusBar()

        self.tabs = QTabWidget()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.tabs)
        self.setLayout(self.mainLayout)
        self.setCentralWidget(self.tabs)

        self.resize(1000, 800)

        if(self.settings.is_not_named()):
            self.show()
            dlg = CreateFarmDialog()
            if dlg.exec():
                self.settings.set_name(dlg.textValue())
            else:
                sys.exit()

        self.update()

    def update(self):
        self.tabs = QTabWidget()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.tabs)
        self.setLayout(self.mainLayout)
        self.setCentralWidget(self.tabs)

        try:
            self.helpWidget.show()
        except:
            self.helpWidget = HelpWidget(self)
            self.addDockWidget(Qt.RightDockWidgetArea, self.helpWidget)

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
                            str(self.settings.get_name()) + " Overview")
        self.tabs.setCurrentIndex(0)
        self.show()
