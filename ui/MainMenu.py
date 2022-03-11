# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (QMenuBar, QVBoxLayout, QLabel, QFormLayout, QTableView)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
import sys

from ui.widgets import (GroupWidget, ScheduleWidget, ExpenseWidget)
from model.data_model import PandasModel
from db.export import Exporter
import os, os.path
import pandas as pd

class MainMenu(QMenuBar):
    def __init__(self, main_window):
        QMenuBar.__init__(self)
        self.main_win = main_window
        self.main_win.setMenuBar(self)

        c_groupAction = QAction("Create Group", self.main_win)
        c_groupAction.triggered.connect(self.c_group)
        c_schedAction = QAction("Create Schedule", self.main_win)
        c_schedAction.triggered.connect(self.c_sched)
        c_expenseAction = QAction("Create Expense", self.main_win)
        c_expenseAction.triggered.connect(self.c_expense)
        exitAction = QAction("Exit", self.main_win)
        exitAction.triggered.connect(self.close_app)
        v_groupAction = QAction("View Groups", self.main_win)
        v_groupAction.triggered.connect(self.v_group)
        v_schedAction = QAction("View Schedules", self.main_win)
        v_schedAction.triggered.connect(self.v_sched)
        v_expenseAction = QAction("View Expenses", self.main_win)
        v_expenseAction.triggered.connect(self.v_expense)
        ex_groupAction = QAction("Show Example Group", self.main_win)
        ex_groupAction.triggered.connect(self.ex_group)
        ex_schedAction = QAction("Show Example Schedule", self.main_win)
        ex_schedAction.triggered.connect(self.ex_sched)
        ex_expenseAction = QAction("Show Example Expense", self.main_win)
        ex_expenseAction.triggered.connect(self.ex_expense)
        ex_groupAction = QAction("Show Example Group", self.main_win)
        ex_groupAction.triggered.connect(self.ex_group)
        help_barAction = QAction("Show Help Bar", self.main_win)
        help_barAction.triggered.connect(self.help_bar)
        # help_barAction = QAction("Show Help Bar", self.main_win)
        # help_barAction.setStatusTip('Help Bar')
        # help_barAction.triggered.connect(self.help_bar)

        self.menu1 = self.addMenu("File")
        self.menu1.addAction(c_groupAction)
        self.menu1.addAction(c_schedAction)
        self.menu1.addAction(c_expenseAction)
        self.menu1.addAction(exitAction)
        self.menu2 = self.addMenu("View")
        self.menu2.addAction(v_groupAction)
        self.menu2.addAction(v_schedAction)
        self.menu2.addAction(v_expenseAction)
        self.menu3 = self.addMenu("Help")
        self.menu3.addAction(ex_groupAction)
        self.menu3.addAction(ex_schedAction)
        self.menu3.addAction(ex_expenseAction)
        self.menu3.addAction(help_barAction)

    def c_group(self):
        self.g_widget = GroupWidget(self.main_win)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.g_widget)
        self.main_win.setLayout(self.mainLayout)
        self.main_win.setCentralWidget(self.g_widget)

    def c_sched(self):
        self.s_widget = ScheduleWidget(self.main_win)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.s_widget)
        self.main_win.setLayout(self.mainLayout)
        self.main_win.setCentralWidget(self.s_widget)

    def c_expense(self):
        self.e_widget = ExpenseWidget(self.main_win)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.e_widget)
        self.main_win.setLayout(self.mainLayout)
        self.main_win.setCentralWidget(self.e_widget)

    def v_group(self):
        self.main_win.layout = QFormLayout()
        self.groups = self.main_win.farm.get_groups()
        model = PandasModel(self.groups)

        farmview = QTableView()
        farmview.resize(500, 300)
        farmview.horizontalHeader().setStretchLastSection(True)
        farmview.setAlternatingRowColors(True)
        farmview.setSelectionBehavior(QTableView.SelectRows)
        farmview.setModel(model)
        self.main_win.layout.addRow(farmview)
        self.main_win.setLayout(self.main_win.layout)
        self.main_win.setCentralWidget(farmview)

    def v_sched(self):
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

    def v_expense(self):
        self.main_win.layout = QFormLayout()
        try:
            folder_path = os.path.join(os.getcwd(), "data")
            farm_filename = os.path.join(folder_path, "expense_db.csv")
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

    def ex_group(self):
        expense_text = QLabel("Please create an expense. Enter the name below:", alignment=Qt.AlignCenter)

        gview = QTableView()
        gview.resize(500, 300)
        gview.horizontalHeader().setStretchLastSection(True)
        gview.setAlternatingRowColors(True)
        gview.setSelectionBehavior(QTableView.SelectRows)
        try:
            g=pd.read_csv("data/examples/ex_group.csv")
            modelg = PandasModel(g)
            gview.setModel(modelg)
            gp_display = gview
        except:
            text = QLabel("No example file found.", alignment=Qt.AlignCenter)
            #button = QPushButton("Welcome to FarmTool!")
            gp_display = text

        self.main_win.setCentralWidget(gp_display)

    def ex_sched(self):
        expense_text = QLabel("Please create an expense. Enter the name below:", alignment=Qt.AlignCenter)
        self.main_win.setCentralWidget(expense_text)

    def ex_expense(self):
        expense_text = QLabel("Please create an expense. Enter the name below:", alignment=Qt.AlignCenter)
        self.main_win.setCentralWidget(expense_text)

    def help_bar(self):
        expense_text = QLabel("Please create an expense. Enter the name below:", alignment=Qt.AlignCenter)
        self.main_win.setCentralWidget(expense_text)

    def close_app(self):
        sys.exit()
