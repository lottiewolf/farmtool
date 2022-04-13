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
    QInputDialog,
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
            table = self.set_table()
            self.v_tabs.addTab(table, g.name)
        self.v_tabs.addTab(self.set_table(), "All")
        self.v_tabs.addTab(self.set_table(), "+")
        self.v_tabs.setCurrentIndex(0)
        self.v_tabs.currentChanged.connect(self.change_tab)
        self.display(0)

    def change_tab(self):
        self.display(self.v_tabs.currentIndex())

    def display(self, gp_i=0):
        # if gp_i is in the range of gps, then get the animals in that group
        if(gp_i < len(self.gps)):
            self.animals = Farm.instance().get_animals(gp_id=self.gps[gp_i].id)
        elif(gp_i == len(self.gps)):
            #this is the second to last tab, display "All" animals
            self.animals = Farm.instance().get_animals()
        elif(gp_i == len(self.gps)+1):
            #this is the last tab, add an animal "+"
            self.animals = []
        else:
            self.animals = []

        model = TableModel(self.animals)
        self.tables[gp_i].setModel(model)
        self.groups.setModel(ListModel(self.gps))
        self.groups.setCurrentIndex(-1)

    def set_table(self):
        t_view = QTableView()
        t_view.resize(500, 300)
        t_view.horizontalHeader().setStretchLastSection(True)
        t_view.setAlternatingRowColors(True)
        t_view.setSelectionBehavior(QTableView.SelectRows)
        self.tables.append(t_view)
        return t_view

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

    def add_group_form(self):
        self.gp_name = QLineEdit()
        self.layout.addRow(QLabel("Group Name"), self.gp_name)
        self.gp_button = QPushButton("Add")
        self.gp_button.setGeometry(QRect(20, 15, 43, 18))
        self.layout.addRow(self.gp_button)
        self.gp_button.clicked.connect(self.add_gp)

    def add_gp(self):
        try:
            self.farm = Farm.instance().add_group(self.gp_name.text())
        except:
            raise Exception("Could not modify groups.")

        self.gp_name.setText("")
        model = TableModel(self.farm)
        self.farmview.setModel(model)

class AddGroupDialog(QInputDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Please create a farm")
        self.setCancelButtonText("Exit Farm Tool")
        self.setOkButtonText("Create Farm")
        self.setLabelText("Please enter the name of your farm: ")
        self.setTextValue("write farm name here")

