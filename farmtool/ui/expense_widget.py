# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QTableView,
    QLineEdit,
    QDoubleSpinBox,
    QComboBox,
    QDateEdit,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import (QRect, QDateTime)
from farmtool.model.table_model import TableModel
from farmtool.model.list_model import ListModel
from farmtool.model.farm_db import FarmDB
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

        self.name = QLineEdit()
        self.cost = QDoubleSpinBox()
        self.cost.setRange(0.0, 1000000)
        self.groups = QComboBox()
        self.animals = QComboBox()
        self.date_added = QDateEdit(calendarPopup=True)
        self.date_added.setDateTime(QDateTime.currentDateTime())

        self.layout.addRow(QLabel("Name of Expense"), self.name)
        self.layout.addRow(QLabel("Cost"), self.cost)
        self.layout.addRow(QLabel("Group"), self.groups)
        self.layout.addRow(QLabel("Animal"), self.animals)
        self.layout.addRow(QLabel("Date Added"), self.date_added)
        self.gp_button = QPushButton("Add")
        self.gp_button.setGeometry(QRect(20, 15, 43, 18))
        self.layout.addRow(self.gp_button)
        self.gp_button.clicked.connect(self.add_expense)

        self.setLayout(self.layout)

    def display(self):
        self.expenses = FarmDB.instance().get_expenses()
        
        hdr = ["Name","Cost","Group", "Animal", "Date"]
        model = TableModel(self.expenses, header=hdr)
        self.farmview.setModel(model)
        self.groups.setModel(ListModel(FarmDB.instance().get_groups()))
        self.groups.setCurrentIndex(-1)
        self.animals.setModel(ListModel(FarmDB.instance().get_animals()))
        self.animals.setCurrentIndex(-1)
        self.name.setText("")
        self.cost.setValue(0.0)

    def add_expense(self):
        g_i = self.groups.currentIndex()
        a_i = self.animals.currentIndex()
        self.expenses = FarmDB.instance().add_expense(
            self.name.text(),
            self.cost.value(),
            self.groups.model().currentObj(g_i),
            self.animals.model().currentObj(a_i),
            self.date_added.date().toPython(),
        )
        self.date_added.setDateTime(QDateTime.currentDateTime())
        self.display()
