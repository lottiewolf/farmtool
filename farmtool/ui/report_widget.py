# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QTableView,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import Qt
from farmtool.model.table_model import TableModel
from farmtool.model.farm_db import FarmDB
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
        self.animals = FarmDB.instance().get_animals(gp_id)
        self.supplies = FarmDB.instance().get_supplies()

        # Create dictionary of supplies
        self.sup_dict = {}
        for sup in self.supplies:
            self.sup_dict[sup.id] = sup

        # Create report table with 0 entries
        self.report = np.zeros([len(self.supplies), len(self.animals)*2])

        # Populate table with cost of each supply per schedule, per animal
        hdr = []
        for a in self.animals:
            print("Here is a row of the animal results:"+str(a))
            hdr.append(a.name)
            sched = FarmDB.instance().get_schedules(a.id)
            for s in sched:
                supply = self.sup_dict[s.supply_id]
                if (supply.purchase_qty != 0):
                    cost_per_day = (supply.price/supply.purchase_qty)*s.qty * s.frequency
                else:
                    cost_per_day = 0
                self.report[self.supplies.index(supply)][self.animals.index(a)] += cost_per_day
        # next rows, get daily expenses per animal
        #            multiply to get montly cost
        #            multiply to get yearly cost
        #
        
        model = TableModel(self.report, header=hdr)

        # Set headers
        for a in self.animals:
            model.setHeaderData(self.animals.index(a), Qt.Horizontal, a.name)
        for s in self.supplies:
            model.setHeaderData(self.supplies.index(s), Qt.Vertical, s.name)

        self.reportview.setModel(model)
