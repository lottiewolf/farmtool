# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QTabWidget)
from PySide6.QtCore import Qt
from farmtool.config.config_farm import ConfigFarm
from farmtool.ui.main_menu import MainMenu
from farmtool.ui.animal_widget import AnimalWidget
from farmtool.ui.schedule_widget import ScheduleWidget
from farmtool.ui.supply_widget import SupplyWidget
from farmtool.ui.expense_widget import ExpenseWidget
from farmtool.ui.report_widget import ReportWidget
from farmtool.ui.help_widget import HelpWidget
from farmtool.ui.create_farm_dialog import CreateFarmDialog
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

        self.show_tabs()

    def show_tabs(self):
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

        self.anim_tab = AnimalWidget()
        self.sched_tab = ScheduleWidget()
        self.supply_tab = SupplyWidget()
        self.expense_tab = ExpenseWidget()
        self.report_tab = ReportWidget()

        self.tabs.addTab(self.anim_tab, "Animals")
        self.tabs.addTab(self.sched_tab, "Schedules")
        self.tabs.addTab(self.supply_tab, "Supplies")
        self.tabs.addTab(self.expense_tab, "Expenses")
        self.tabs.addTab(self.report_tab, "Report")
        self.tabs.setCurrentIndex(0)
        self.tabs.currentChanged.connect(self.change_tab)
        self.tabs.currentWidget().display()

        self.setWindowTitle(self.title_version + "  -  " +
                            str(self.settings.get_name()) + " Overview")
        self.show()

    def change_tab(self):
        self.tabs.currentWidget().display()
