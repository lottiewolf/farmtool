# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QWidget,
    QTabWidget,
    QVBoxLayout,
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

        # Set layout to vertical tabs, which displays groups' names
        self.v_tabs = QTabWidget()
        self.v_tabs.setTabPosition(QTabWidget.West)
        self.layout = QFormLayout()
        self.layout.addWidget(self.v_tabs)
        self.setLayout(self.layout)

        # Create form for Add Animal on layout
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

        # Get list of groups to add to tabs
        try:
            self.gps = Farm.instance().get_groups()
        except:
            self.gps = []
        # if the list is empty, add the "Main Barn" group
        self.tables = []
        for g in self.gps:
            # Set table view, which will display animals (of a group)
            t_view = QTableView()
            t_view.resize(500, 300)
            t_view.horizontalHeader().setStretchLastSection(True)
            t_view.setAlternatingRowColors(True)
            t_view.setSelectionBehavior(QTableView.SelectRows)
            self.tables.append(t_view)
            self.v_tabs.addTab(t_view, g.name)

        self.update_anim()

    def update_anim(self, gp_i=0):
        try:
            self.animals = Farm.instance().get_animals(gp_id=self.gps[gp_i].id)
        except:
            self.animals = []

        model = TableModel(self.animals)
        self.tables[gp_i].setModel(model)
        self.groups.setModel(ListModel(self.gps))
        self.groups.setCurrentIndex(-1)

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
        self.groups.setCurrentIndex(-1)
        self.date_added.setDateTime(QDateTime.currentDateTime())
        #model = TableModel(self.animals)
        #self.farmview.setModel(model)

