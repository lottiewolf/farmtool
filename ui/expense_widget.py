# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, QSpinBox, QDateEdit, QPushButton, QCalendarWidget)
from PySide6.QtWidgets import (QGroupBox, QTableView, QFormLayout)
from PySide6.QtCore import (Qt, QRect, QDateTime)
from ui.pandas_model import PandasModel
from controller.farm import Farm
import pandas as pd

class ExpenseWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.layout = QFormLayout()

        self.farmview = QTableView()
        self.farmview.resize(500, 300)
        self.farmview.horizontalHeader().setStretchLastSection(True)
        self.farmview.setAlternatingRowColors(True)
        self.farmview.setSelectionBehavior(QTableView.SelectRows)
        self.layout.addRow(self.farmview)

        self.ex_name = QLineEdit()
        self.ex_cost = QLineEdit()
        self.ex_group = QLineEdit()
        self.ex_animal = QLineEdit()
        self.ex_supply = QLineEdit()
        self.layout.addRow(QLabel("Name of Expense"), self.ex_name)
        self.layout.addRow(QLabel("Cost"), self.ex_cost)
        self.layout.addRow(QLabel("Group"), self.ex_group)
        self.layout.addRow(QLabel("Animal"), self.ex_animal)
        self.layout.addRow(QLabel("Supply"), self.ex_supply)
        self.gp_button = QPushButton("Add")
        self.gp_button.setGeometry(QRect(20, 15, 43, 18))
        self.layout.addRow(self.gp_button)
        self.gp_button.clicked.connect(self.add_expense)

        self.setLayout(self.layout)

        self.update_expense()

    def update_expense(self):
        try:
            self.expenses = Farm.instance().get_expenses()
        except:
            self.expenses = pd.DataFrame()

        model = PandasModel(self.expenses)
        self.farmview.setModel(model)

    def add_expense(self):
        try:
            self.expenses = Farm.instance().add_expense(self.ex_name.text(), self.ex_cost.text(), self.ex_group.text(), self.ex_animal.text(), self.ex_supply.text())
        except:
            raise Exception("Could not modify expenses.")

        self.ex_name.setText("")
        self.ex_cost.setText("")
        self.ex_group.setText("")
        self.ex_animal.setText("")
        self.ex_supply.setText("")
        model = PandasModel(self.expenses)
        self.farmview.setModel(model)
