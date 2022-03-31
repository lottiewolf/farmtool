# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (QMenuBar, QVBoxLayout, QLabel, QFormLayout, QTableView, QMessageBox)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from ui.group_widget import GroupWidget
from ui.schedule_widget import ScheduleWidget
from ui.expense_widget import ExpenseWidget
from model.pandas_model import PandasModel
from controller.farm import Farm
import pandas as pd
import os, os.path
import sys


class MainMenu(QMenuBar):
    def __init__(self, main_window):
        QMenuBar.__init__(self)
        self.main_win = main_window
        self.main_win.setMenuBar(self)

        # Create File menu
        i_dataAction = QAction("Import Data", self.main_win)
        i_dataAction.triggered.connect(self.i_data)
        e_dataAction = QAction("Export Data", self.main_win)
        e_dataAction.triggered.connect(self.e_data)
        exitAction = QAction("Exit", self.main_win)
        exitAction.triggered.connect(self.close_app)
        self.menu1 = self.addMenu("File")
        self.menu1.addAction(i_dataAction)
        self.menu1.addAction(e_dataAction)
        self.menu1.addAction(exitAction)

        # Create View menu
        overviewAction = QAction("Farm Overview", self.main_win)
        overviewAction.triggered.connect(self.overview)
        rep_listAction = QAction("Expense Report - List", self.main_win)
        rep_listAction.triggered.connect(self.rep_list)
        rep_plotAction = QAction("Expense Report - Plot", self.main_win)
        rep_plotAction.triggered.connect(self.rep_plot)
        self.menu2 = self.addMenu("View")
        self.menu2.addAction(overviewAction)
        self.menu2.addAction(rep_listAction)
        self.menu2.addAction(rep_plotAction)

        #Create Help menu
        help_barAction = QAction("Show Help Bar", self.main_win)
        help_barAction.triggered.connect(self.help_bar)
        aboutAction = QAction("About Software", self.main_win)
        aboutAction.triggered.connect(self.about_app)
        self.menu3 = self.addMenu("Help")
        self.menu3.addAction(help_barAction)
        self.menu3.addAction(aboutAction)

    def i_data(self):
        self.gp_dlg = CreateGroupDialog()
        if self.gp_dlg.exec():
            Farm.instance().add_group(self.gp_dlg.textValue())

        self.g_widget = GroupWidget()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.g_widget)
        self.main_win.setLayout(self.mainLayout)
        self.main_win.setCentralWidget(self.g_widget)

    def e_data(self):
        self.gp_dlg = CreateGroupDialog()
        if self.gp_dlg.exec():
            Farm.instance().add_group(self.gp_dlg.textValue())

        self.s_widget = ScheduleWidget(self.main_win)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.s_widget)
        self.main_win.setLayout(self.mainLayout)
        self.main_win.setCentralWidget(self.s_widget)

    def close_app(self):
        sys.exit()

    def overview(self):
        #self.main_win.show()
        pass

    def rep_list(self):
        self.main_win.layout = QFormLayout()
        model = PandasModel(Farm.instance().get_groups())

        farmview = QTableView()
        farmview.resize(500, 300)
        farmview.horizontalHeader().setStretchLastSection(True)
        farmview.setAlternatingRowColors(True)
        farmview.setSelectionBehavior(QTableView.SelectRows)
        farmview.setModel(model)
        self.main_win.layout.addRow(farmview)
        self.main_win.setLayout(self.main_win.layout)
        self.main_win.setCentralWidget(farmview)

    def rep_plot(self):
        self.main_win.layout = QFormLayout()
        try:
            folder_path = os.path.join(os.getcwd(), "data")
            farm_filename = os.path.join(folder_path, "schedule_db.csv")
            df=pd.read_csv(farm_filename)
            model = PandasModel(df)

            farmview = QTableView()
            farmview.resize(500, 300)
            farmview.horizontalHeader().setStretchLastSection(True)
            farmview.setAlternatingRowColors(True)
            farmview.setSelectionBehavior(QTableView.SelectRows)
            farmview.setModel(model)
            self.main_win.layout.addRow(farmview)
        except:
            farmview = QTableView()
            farmview = QLabel("An error has occurred", alignment=Qt.AlignCenter)
        self.main_win.setLayout(self.main_win.layout)
        self.main_win.setCentralWidget(farmview)

    def help_bar(self):
        self.main_win.helpWidget.show()

    def about_app(self):
        self.about_dlg = QMessageBox()
        self.about_dlg.setText("This is version 0.1 of the Farm Tool app. To learn more, please visit: \n https://github.com/lottiewolf/farmtool/")
        self.about_dlg.setWindowTitle("Farm Tool - About")
        self.about_dlg.show()


