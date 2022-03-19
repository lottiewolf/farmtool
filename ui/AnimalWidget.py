# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (QWidget, QFormLayout, QLabel, QLineEdit, QComboBox, QSpinBox, QDateEdit, QPushButton, QCalendarWidget)
from PySide6.QtCore import (Qt, QRect, QDateTime)
from PySide6.QtWidgets import (QGroupBox, QTableView, QFormLayout)
from model.data_model import PandasModel
from ui.Config import Config
from model.farm_model import Farm
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
        # This dropdown should be populated from a model, subclassed from QAbstractListModel.
        # This should be done in Farm or Group or Animals, or perhaps a new class?
        self.groups_list.addItems(self.get_group_list())
        # The above line is terrible and should be replaced a model mechanism

        #print(self.groups_list.model())
        #print(self.groups_list.view())
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
            self.groups = Farm.instance().get_groups()
        except:
            self.animals = pd.DataFrame()

        model = PandasModel(self.animals)
        self.farmview.setModel(model)

    def add_anim(self):
        try:
            self.animals = Farm.instance().add_animal(self.anim_name.text(), self.groups_list.currentText(), self.date_added.date(), None)
        except:
            raise Exception("Could not modify animals.")

        self.anim_name.setText("")
        self.groups_list.clear()
        self.groups_list.addItems(self.get_group_list())
        self.date_added.setDateTime(QDateTime.currentDateTime())
        model = PandasModel(self.animals)
        self.farmview.setModel(model)

    def get_group_list(self):
        try:
            self.update_anim()
            self.g_list = self.groups.name.tolist()
        except:
            self.g_list = []
        return self.g_list
