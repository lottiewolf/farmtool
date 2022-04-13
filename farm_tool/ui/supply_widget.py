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
from farm_tool.model.table_model import TableModel
from farm_tool.controller.farm import Farm
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

        self.display()

    def display(self):
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
                self.price.value(),
                self.purchase_qty.value(),
                self.units.currentText(),
                self.notes.toPlainText(),
                self.p_date.date().toPython(),
                self.file,
            )
        except:
            raise Exception("Could not modify supplies.")

        self.supply_name.setText("")
        self.price.setValue(0.0)
        self.purchase_qty.setValue(0.0)
        self.units.setCurrentIndex(0)
        self.notes.setText("")
        self.p_date.setDateTime(QDateTime.currentDateTime())
        model = TableModel(self.supplies)
        self.farmview.setModel(model)
