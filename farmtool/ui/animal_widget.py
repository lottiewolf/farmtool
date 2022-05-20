# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QWidget,
    QTreeView,
    QTabWidget,
    QGroupBox,
    QVBoxLayout,
    QFormLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QPushButton,
    QTableView,
    QInputDialog,
)
from PySide6.QtCore import (QRect, QDateTime)
from farmtool.model.table_model import TableModel
from farmtool.model.list_model import ListModel
from farmtool.model.farm_db import FarmDB
import pandas as pd


class AnimalWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # Create layout for all the widgets
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Create vertical tabs, which will display groups' names
        self.v_tabs = QTabWidget()
        
        self.layout.addWidget(self.v_tabs)
        
        # Get list of groups to add to tabs
        try:
            self.gps = FarmDB.instance().get_groups()
        except:
            self.gps = []
        if(len(self.gps)==0):
            self.gps = FarmDB.instance().add_group("Main Barn")
        
        print("Here are the groups:"+str(self.gps))
        self.tables = []
        for g in self.gps:
            # Set table view, which will display animals (of a group)
            table = self.set_table()
            self.tables.append(table)
            self.v_tabs.addTab(table, g.name)
        all_table = self.set_table()
        self.tables.append(all_table)
        self.v_tabs.addTab(all_table, "All")

        # Create form for Add Animal
        self.a_form_layout = QGridLayout()
        self.name = QLineEdit()
        self.groups = QComboBox()
        self.date_added = QDateEdit(calendarPopup=True)
        self.date_added.setDateTime(QDateTime.currentDateTime())
        self.a_form_layout.addWidget(QLabel("Animal Name"), 0, 0)
        self.a_form_layout.addWidget(self.name, 0, 1)
        self.a_form_layout.addWidget(QLabel("Group Name"), 0, 2)
        self.a_form_layout.addWidget(self.groups, 0, 3)
        self.a_form_layout.addWidget(QLabel("Date Added"), 0, 4)
        self.a_form_layout.addWidget(self.date_added, 0, 5)
        self.gp_button = QPushButton("Add")
        self.gp_button.setGeometry(QRect(20, 15, 43, 18))
        self.a_form_layout.addWidget(self.gp_button, 0, 6)
        self.gp_button.clicked.connect(self.add_anim)       
        self.a_form_box = QGroupBox("Add New Animal", self)
        self.a_form_box.setLayout(self.a_form_layout)
        self.layout.addWidget(self.a_form_box)

        # Create form for Add Group
        self.g_form_layout = QGridLayout()
        self.gp_name = QLineEdit()
        self.g_form_layout.addWidget(QLabel("Group Name"), 0, 0)
        self.g_form_layout.addWidget(self.gp_name, 0, 1)
        self.gp_button = QPushButton("Add")
        self.gp_button.setGeometry(QRect(20, 15, 43, 18))
        self.g_form_layout.addWidget(self.gp_button, 0, 2)
        self.gp_button.clicked.connect(self.add_gp)
        self.g_form_box = QGroupBox("Add New Group", self)
        self.g_form_box.setLayout(self.g_form_layout)
        self.layout.addWidget(self.g_form_box)
        
        self.v_tabs.setTabPosition(QTabWidget.West)
        self.v_tabs.currentChanged.connect(self.change_tab)

    def change_tab(self):
        self.display(self.v_tabs.currentIndex())
        
    def display(self, index=0):
        self.v_tabs.setCurrentIndex(index)       
        # if index is in the range of gps, then get the animals in that group
        if(index < len(self.tables)-1):
            self.animals = FarmDB.instance().get_animals(gp_id=self.gps[index].id)
        elif(index == len(self.tables)-1):
            #this is the last tab, display "All" animals
            self.animals = FarmDB.instance().get_animals()
        else:
            self.animals = []

        hdr = ["Name", "Group", "Date Added", "Date Removed"]
        model = TableModel(self.animals, header=hdr)
        self.tables[index].setModel(model)
        self.groups.setModel(ListModel(self.gps))
        self.groups.setCurrentIndex(-1)

    def set_table(self):
        t_view = QTableView()
        t_view.resize(500, 300)
        t_view.horizontalHeader().setStretchLastSection(True)
        t_view.setAlternatingRowColors(True)
        t_view.setSelectionBehavior(QTableView.SelectRows)
        return t_view

    def add_anim(self):
        i = self.groups.currentIndex()
        try:
            self.animals = FarmDB.instance().add_animal(
                self.name.text(),
                self.groups.model().currentObj(i),
                self.date_added.date().toPython(),
                self.date_added.date().toPython(),
            )
        except:
            raise Exception("Could not modify animals.")

        self.name.setText("")
        self.groups.setModel(ListModel(self.gps))
        self.groups.setCurrentIndex(-1)
        self.date_added.setDateTime(QDateTime.currentDateTime())
        self.display(i)

    def add_gp(self):
        self.gps = FarmDB.instance().add_group(self.gp_name.text())
        new_table = self.set_table()
        self.v_tabs.insertTab(len(self.gps)-1, new_table, self.gp_name.text())
        self.tables.insert(-2, new_table)
        self.gp_name.setText("")
        self.display(len(self.gps)-1)
