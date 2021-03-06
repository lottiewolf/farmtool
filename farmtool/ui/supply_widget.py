# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QGridLayout,
    QTableView,
    QLabel,
    QLineEdit,
    QDateEdit,
    QComboBox,
    QFileDialog,
    QPushButton,
    QDoubleSpinBox,
    QTextEdit,
)
from PySide6.QtCore import (QRect, QDateTime)
from farmtool.model.table_model import TableModel
from farmtool.model.farm_db import FarmDB
import pandas as pd


class SupplyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.layout = QFormLayout()

        # This section sets the top view, displays all the supplies in a table
        self.farmview = QTableView()
        self.farmview.resize(500, 300)
        self.farmview.horizontalHeader().setStretchLastSection(True)
        self.farmview.setAlternatingRowColors(True)
        self.farmview.setSelectionBehavior(QTableView.SelectRows)
        self.layout.addRow(self.farmview)

        # This section sets the bottom view, a form for adding a new supply
        self.add_layout = QGridLayout()
        self.supply_name = QLineEdit()
        self.purchase_qty = QDoubleSpinBox()
        self.purchase_qty.setRange(0.0, 1000000)
        self.units = QComboBox()
        self.units.addItems(["lbs", "oz", "tablets", "flakes", "bales", "yards", "item"])
        self.units.setCurrentIndex(-1)
        self.price = QDoubleSpinBox()
        self.price.setRange(0.0, 1000000)
        self.notes = QTextEdit()
        self.p_date = QDateEdit(calendarPopup=True)
        self.p_date.setDateTime(QDateTime.currentDateTime())
        self.inv_image = QFileDialog()
        self.inv_button = QPushButton("Browse")
        self.file = "file name"
        # add Browse button that brings up QFileDialog...
        self.add_layout.addWidget(QLabel("Supply Name"), 0, 0)
        self.add_layout.addWidget(self.supply_name, 0, 1, 1, 5)
        self.add_layout.addWidget(QLabel("Purchase Price"), 1, 0)
        self.add_layout.addWidget(self.price, 1, 1)
        self.add_layout.addWidget(QLabel("Purchase Quantity"), 1, 2)
        self.add_layout.addWidget(self.purchase_qty, 1, 3)
        self.add_layout.addWidget(QLabel("Units"), 1, 4)
        self.add_layout.addWidget(self.units, 1, 5)
        self.add_layout.addWidget(QLabel("Notes"), 2, 0)
        self.add_layout.addWidget(self.notes, 2, 1, 1, 5)
        self.add_layout.addWidget(QLabel("Purchase Date"), 3, 0)
        self.add_layout.addWidget(self.p_date, 3, 1)
        self.add_layout.addWidget(QLabel("Add Invoice"), 3, 2)
        self.add_layout.addWidget(self.inv_button, 3, 3)
        self.gp_button = QPushButton("Add")
        self.gp_button.setGeometry(QRect(20, 15, 43, 18))
        self.add_layout.addWidget(self.gp_button, 5, 0)
        self.gp_button.clicked.connect(self.add_supply)
        self.layout.addRow(self.add_layout)

        self.setLayout(self.layout)

    def display(self):
        self.supplies = FarmDB.instance().get_supplies()
        
        hdr = ["Id", "Name","Price","Qty", "Units", "Notes", "Date", "Invoice"]
        model = TableModel(self.supplies, header=hdr)
        self.farmview.setModel(model)
        self.supply_name.setText("")
        self.price.setValue(0.0)
        self.purchase_qty.setValue(0.0)
        self.units.setCurrentIndex(0)
        self.notes.setText("")
        self.p_date.setDateTime(QDateTime.currentDateTime())

    def add_supply(self):
        #also should pass an image of receipt
        self.supplies = FarmDB.instance().add_supply(
            self.supply_name.text(),
            self.price.value(),
            self.purchase_qty.value(),
            self.units.currentText(),
            self.notes.toPlainText(),
            self.p_date.date().toPython(),
            self.file,
        )
        self.display()
