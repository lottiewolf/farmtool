# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QTableView,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox,
    QDateEdit,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import (QRect, QDateTime)
from model.pandas_model import PandasModel
from model.list_model import ListModel
from controller.farm import Farm
import pandas as pd


class ScheduleWidget(QWidget):
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
        self.animals = QComboBox()
        self.supplies = QComboBox()
        self.qty = QDoubleSpinBox()
        self.date_start = QDateEdit(calendarPopup=True)
        self.date_start.setDateTime(QDateTime.currentDateTime())

        self.layout.addRow(QLabel("Schedule Name"), self.name)
        self.layout.addRow(QLabel("Animal"), self.animals)
        self.layout.addRow(QLabel("Supply"), self.supplies)
        self.layout.addRow(QLabel("Quantity"), self.qty)
        self.layout.addRow(QLabel("Date Started"), self.date_start)
        self.gp_button = QPushButton("Add")
        self.gp_button.setGeometry(QRect(20, 15, 43, 18))
        self.layout.addRow(self.gp_button)
        self.gp_button.clicked.connect(self.add_sched)

        self.setLayout(self.layout)

        self.update_sched()

    def update_sched(self):
        try:
            self.schedules = Farm.instance().get_schedules()
        except:
            self.schedules = pd.DataFrame()

        model = PandasModel(self.schedules)
        self.farmview.setModel(model)
        self.animals.setModel(ListModel(Farm.instance().get_animals()))
        self.supplies.setModel(ListModel(Farm.instance().get_supplies()))

    def add_sched(self):
        a_i = self.animals.currentIndex()
        s_i = self.supplies.currentIndex()
        try:
            self.schedules = Farm.instance().add_schedule(
                self.name.text(),
                self.animals.model().currentObj(a_i),
                self.supplies.model().currentObj(s_i),
                self.qty.value(),
                self.date_start.date().toPython(),
            )
        except:
            raise Exception("Could not modify schedules.")

        self.name.setText("")
        self.animals.setModel(ListModel(Farm.instance().get_animals()))
        self.supplies.setModel(ListModel(Farm.instance().get_supplies()))
        self.qty.setValue(0.0)
        self.date_start.setDateTime(QDateTime.currentDateTime())
        model = PandasModel(self.schedules)
        self.farmview.setModel(model)
