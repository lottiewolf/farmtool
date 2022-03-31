# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (QGroupBox, QTableView, QFormLayout)
from PySide6.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, QSpinBox, QDateEdit, QPushButton, QCalendarWidget)
from PySide6.QtCore import (Qt, QRect, QDateTime)
from model.pandas_model import PandasModel
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

        self.sched_name = QLineEdit()
        self.sched_anim = QLineEdit()
        self.sched_supply = QLineEdit()
        self.sched_qty = QLineEdit()
        self.sched_date_start = QDateEdit(calendarPopup=True)
        self.sched_date_start.setDateTime(QDateTime.currentDateTime())
        self.layout.addRow(QLabel("Schedule Name"), self.sched_name)
        self.layout.addRow(QLabel("Animal Name"), self.sched_anim)
        self.layout.addRow(QLabel("Supply"), self.sched_supply)
        self.layout.addRow(QLabel("Quantity"), self.sched_qty)
        self.layout.addRow(QLabel("Date Started"), self.sched_date_start)
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

    def add_sched(self):
        try:
            self.schedules = Farm.instance().add_schedule(self.sched_name.text(), self.sched_anim.text(), self.sched_supply.text(), self.sched_qty.text(), self.sched_date_start.date())
        except:
            raise Exception("Could not modify schedules.")

        self.sched_name.setText("")
        self.sched_anim.setText("")
        self.sched_supply.setText("")
        self.sched_qty.setText("")
        self.sched_date_start.setDateTime(QDateTime.currentDateTime())
        model = PandasModel(self.schedules)
        self.farmview.setModel(model)
