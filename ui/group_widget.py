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
from model.pandas_model import PandasModel
from controller.farm import Farm
import pandas as pd


class GroupWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.layout = QFormLayout()

        self.farmview = QTableView()
        self.farmview.resize(500, 300)
        self.farmview.horizontalHeader().setStretchLastSection(True)
        self.farmview.setAlternatingRowColors(True)
        self.farmview.setSelectionBehavior(QTableView.SelectRows)
        self.layout.addRow(self.farmview)

        self.gp_name = QLineEdit()
        self.layout.addRow(QLabel("Group Name"), self.gp_name)
        self.gp_button = QPushButton("Add")
        self.gp_button.setGeometry(QRect(20, 15, 43, 18))
        self.layout.addRow(self.gp_button)
        self.gp_button.clicked.connect(self.add_gp)

        self.setLayout(self.layout)

        self.update_gp()

    def update_gp(self):
        try:
            self.farm = Farm.instance().get_groups()
        except:
            self.farm = pd.DataFrame()

        print("group widget:"+str(self.farm[0]))
        model = PandasModel(self.farm)
        self.farmview.setModel(model)

    def add_gp(self):
        try:
            self.farm = Farm.instance().add_group(self.gp_name.text())
        except:
            raise Exception("Could not modify groups.")

        self.gp_name.setText("")
        model = PandasModel(self.farm)
        self.farmview.setModel(model)
