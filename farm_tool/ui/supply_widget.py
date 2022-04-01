# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QTableView,
    QLabel,
    QLineEdit,
    QPushButton,
    QDoubleSpinBox,
)
from PySide6.QtCore import QRect
from farm_tool.model.table_model import TableModel
from farm_tool.controller.farm import Farm
import pandas as pd


class SupplyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.layout = QFormLayout()

        self.farmview = QTableView()
        self.farmview.resize(500, 300)
        self.farmview.horizontalHeader().setStretchLastSection(True)
        self.farmview.setAlternatingRowColors(True)
        self.farmview.setSelectionBehavior(QTableView.SelectRows)
        self.layout.addRow(self.farmview)

        self.supply_name = QLineEdit()
        self.purchase_qty = QDoubleSpinBox()
        self.units = QLineEdit()
        self.price = QDoubleSpinBox()
        self.notes = QLineEdit()
        self.serving_qty = QDoubleSpinBox()
        self.layout.addRow(QLabel("Supply Name"), self.supply_name)
        self.layout.addRow(QLabel("Purchase Quantity"), self.purchase_qty)
        self.layout.addRow(QLabel("Units"), self.units)
        self.layout.addRow(QLabel("Price"), self.price)
        self.layout.addRow(QLabel("Notes"), self.notes)
        self.layout.addRow(QLabel("Serving Quantity"), self.serving_qty)
        self.gp_button = QPushButton("Add")
        self.gp_button.setGeometry(QRect(20, 15, 43, 18))
        self.layout.addRow(self.gp_button)
        self.gp_button.clicked.connect(self.add_supply)

        self.setLayout(self.layout)

        self.update_supply()

    def update_supply(self):
        try:
            self.supplies = Farm.instance().get_supplies()
        except:
            self.supplies = pd.DataFrame()

        model = TableModel(self.supplies)
        self.farmview.setModel(model)

    def add_supply(self):
        try:
            #also should pass an image of receipt
            self.supplies = Farm.instance().add_supply(
                self.supply_name.text(),
                self.purchase_qty.value(),
                self.units.text(),
                self.price.value(),
                self.notes.text(),
                self.serving_qty.value(),
            )
        except:
            raise Exception("Could not modify supplies.")

        self.supply_name.setText("")
        self.purchase_qty.setValue(0.0)
        self.units.setText("")
        self.price.setValue(0.0)
        self.notes.setText("")
        self.serving_qty.setValue(0.0)
        model = TableModel(self.supplies)
        self.farmview.setModel(model)
