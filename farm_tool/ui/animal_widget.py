# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QPushButton,
    QTableView,
)
from PySide6.QtCore import (QRect, QDateTime)
from farm_tool.model.table_model import TableModel
from farm_tool.model.list_model import ListModel
from farm_tool.controller.farm import Farm
import pandas as pd


class AnimalWidget(QWidget):
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
        self.groups = QComboBox()
        self.date_added = QDateEdit(calendarPopup=True)
        self.date_added.setDateTime(QDateTime.currentDateTime())

        self.layout.addRow(QLabel("Animal Name"), self.name)
        self.layout.addRow(QLabel("Group Name"), self.groups)
        self.layout.addRow(QLabel("Date Added"), self.date_added)
        self.gp_button = QPushButton("Add")
        self.gp_button.setGeometry(QRect(20, 15, 43, 18))
        self.layout.addRow(self.gp_button)
        self.gp_button.clicked.connect(self.add_anim)

        self.setLayout(self.layout)

        self.update_anim()

    def update_anim(self):
        try:
            self.animals = Farm.instance().get_animals()
        except:
            self.animals = pd.DataFrame()

        model = TableModel(self.animals)
        self.farmview.setModel(model)
        self.groups.setModel(ListModel(Farm.instance().get_groups()))

    def add_anim(self):
        i = self.groups.currentIndex()
        try:
            self.animals = Farm.instance().add_animal(
                self.name.text(),
                self.groups.model().currentObj(i),
                self.date_added.date().toPython(),
                self.date_added.date().toPython(),
            )
        except:
            raise Exception("Could not modify animals.")

        self.name.setText("")
        self.groups.setModel(ListModel(Farm.instance().get_groups()))
        self.date_added.setDateTime(QDateTime.currentDateTime())
        model = TableModel(self.animals)
        self.farmview.setModel(model)

