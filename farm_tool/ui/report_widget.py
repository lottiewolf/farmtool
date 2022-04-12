# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QTableView,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import QRect
from farm_tool.model.table_model import TableModel
from farm_tool.controller.farm import Farm
import pandas as pd


class ReportWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.layout = QFormLayout()

        self.farmview = QTableView()
        self.farmview.resize(500, 300)
        self.farmview.horizontalHeader().setStretchLastSection(True)
        self.farmview.setAlternatingRowColors(True)
        self.farmview.setSelectionBehavior(QTableView.SelectRows)
        self.layout.addRow(self.farmview)

        #self.gp_name = QLineEdit()
        #self.layout.addRow(QLabel("Group Name"), self.gp_name)
        #self.gp_button = QPushButton("Add")
        #self.gp_button.setGeometry(QRect(20, 15, 43, 18))
        #self.layout.addRow(self.gp_button)
        #self.gp_button.clicked.connect(self.add_gp)

        self.setLayout(self.layout)

        self.show_gp_report(1)

    def show_gp_report(self, gp_id):
        # first row, get list of animals
        #
        # next rows, get daily expenses per animal
        #            multiply to get montly cost
        #            multiply to get yearly cost
        #
        # in a grid, for each animal, for each supply, display cost
        try:
            self.farm = Farm.instance().get_animals(gp_id)
        except:
            self.farm = pd.DataFrame()

        model = TableModel(self.farm)
        self.farmview.setModel(model)
