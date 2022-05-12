# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QTableView,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import (QRect, Qt)
from farmtool.model.table_model import TableModel
from farmtool.controller.farm import Farm
import pandas as pd
import numpy as np


class ReportWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.layout = QFormLayout()

        self.reportview = QTableView()
        #self.reportview.setHorizontalHeader(QHeaderView)
        #self.reportview.setVerticalHeader(QHeaderView)
        self.reportview.resize(500, 300)
        self.reportview.horizontalHeader().setStretchLastSection(True)
        self.reportview.setAlternatingRowColors(True)
        self.reportview.setSelectionBehavior(QTableView.SelectRows)
        self.layout.addRow(self.reportview)

        self.setLayout(self.layout)

    def display(self, gp_id=1):

        # Get animals of chosen group, get all supplies
        self.animals = Farm.instance().get_animals(gp_id)
        self.supplies = Farm.instance().get_supplies()

        # Create dictionary of supplies
        self.sup_dict = {}
        for sup in self.supplies:
            self.sup_dict[sup.id] = sup

        # Create report table with 0 entries
        self.report = np.zeros([len(self.supplies), len(self.animals)])

        # Populate table with cost of each supply per schedule, per animal
        for a in self.animals:
            sched = Farm.instance().get_schedules(a.id)
            for s in sched:
                supply = self.sup_dict[s.supply_id]
                cost_per_day = (supply.price/supply.purchase_qty)*s.qty * s.frequency
                self.report[self.supplies.index(supply)][self.animals.index(a)] += cost_per_day
        # next rows, get daily expenses per animal
        #            multiply to get montly cost
        #            multiply to get yearly cost
        #

        model = TableModel(self.report)

        # Set headers
        for a in self.animals:
            model.setHeaderData(self.animals.index(a), Qt.Horizontal, a.name)
        for s in self.supplies:
            model.setHeaderData(self.supplies.index(s), Qt.Vertical, s.name)

        self.reportview.setModel(model)
