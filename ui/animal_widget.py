# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QPushButton,
    QCalendarWidget,
    QTableView,
    QGroupBox,
)
from PySide6.QtCore import (QRect, QDateTime)
from model.pandas_model import PandasModel
from model.list_model import ListModel
from controller.farm import Farm
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

        self.anim_name = QLineEdit()
        self.groups_list = QComboBox()
        self.groups_list.setModel(ListModel(Farm.instance().get_groups()))
        self.date_added = QDateEdit(calendarPopup=True)
        self.date_added.setDateTime(QDateTime.currentDateTime())

        self.layout.addRow(QLabel("Animal Name"), self.anim_name)
        self.layout.addRow(QLabel("Group Name"), self.groups_list)
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

        model = PandasModel(self.animals)
        self.farmview.setModel(model)

    def add_anim(self):
        j = self.groups_list.currentIndex()
        try:
            self.animals = Farm.instance().add_animal(
                self.anim_name.text(),
                self.groups_list.model().currentObj(j),
                self.date_added.date().toPython(),
                self.date_added.date().toPython(),
            )
        except:
            raise Exception("Could not modify animals.")

        self.anim_name.setText("")
        self.groups_list.clear()
        self.groups_list.addItems(Farm.instance().get_group_list())
        self.date_added.setDateTime(QDateTime.currentDateTime())
        model = PandasModel(self.animals)
        self.farmview.setModel(model)

