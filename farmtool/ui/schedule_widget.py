# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QTextEdit,
    QSplitter,
    QFormLayout,
    QGridLayout,
    QTableView,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox,
    QDateEdit,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import (Qt, QRect, QDateTime)
from farmtool.model.table_model import TableModel
from farmtool.model.list_model import ListModel
from farmtool.model.farm_db import FarmDB


class ScheduleWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # This section lays out the three splitter windows        
        self.layout = QFormLayout()
        splitter_top = QSplitter(Qt.Horizontal)
        splitter_wholepage = QSplitter(Qt.Vertical)
        splitter_wholepage.addWidget(splitter_top)
        self.layout.addRow(splitter_wholepage)
        
        # This section sets the top view, displays all the schedules in a table
        self.schedview = QTableView()
        self.schedview.resize(500, 300)
        self.schedview.horizontalHeader().setStretchLastSection(True)
        self.schedview.setAlternatingRowColors(True)
        self.schedview.setSelectionBehavior(QTableView.SelectRows)
        splitter_top.addWidget(self.schedview)
        textedit = QTextEdit()
        splitter_top.addWidget(textedit)
        splitter_top.setSizes([100,200])   
        
        # This section sets the bottom view, a form for adding a new schedule
        self.bottom_widget = QFrame()
        self.add_layout = QGridLayout()
        self.name = QLineEdit()
        self.animals = QComboBox()
        self.supplies = QComboBox()
        self.qty = QDoubleSpinBox()
        self.qty.setRange(0.0, 1000000)
        self.units = QLabel("")
        self.notes = QLabel("")
        self.fq = QComboBox()
        self.start_date = QDateEdit(calendarPopup=True)
        self.start_date.setDateTime(QDateTime.currentDateTime())
        self.end_date = QDateEdit(calendarPopup=True)
        self.end_date.setDateTime(QDateTime.currentDateTime())
        self.add_layout.addWidget(QLabel("Schedule Name"), 0, 0)
        self.add_layout.addWidget(self.name, 0, 1)
        self.add_layout.addWidget(QLabel("Animal"), 0, 2)
        self.add_layout.addWidget(self.animals, 0, 3)
        self.add_layout.addWidget(QLabel("Supply"), 1, 0)
        self.add_layout.addWidget(self.supplies, 1, 1)
        self.supplies.currentIndexChanged.connect(self.show_units)
        self.add_layout.addWidget(QLabel("Quantity"), 1, 2)
        self.add_layout.addWidget(self.qty, 1, 3)
        self.add_layout.addWidget(self.units, 1, 4)
        self.add_layout.addWidget(self.notes, 2, 1)
        self.add_layout.addWidget(QLabel("Frequency"), 3, 0)
        self.add_layout.addWidget(self.fq, 3, 1)
        self.add_layout.addWidget(QLabel("Start Date"), 3, 2)
        self.add_layout.addWidget(self.start_date, 3, 3)
        self.add_layout.addWidget(QLabel("End Date"), 3, 4)
        self.add_layout.addWidget(self.end_date, 3, 5)
        self.gp_button = QPushButton("Add")
        self.gp_button.setGeometry(QRect(20, 15, 43, 18))
        self.add_layout.addWidget(self.gp_button, 4, 0)
        self.gp_button.clicked.connect(self.add_sched)
        self.bottom_widget.setLayout(self.add_layout)      
        splitter_wholepage.addWidget(self.bottom_widget)

        self.setLayout(self.layout)

    def display(self):
        self.schedules = FarmDB.instance().get_schedules()
        
        hdr = ["Name","Animal","Supply", "Qty", "Frequency", "Start", "End"]
        model = TableModel(self.schedules, header=hdr)
        self.schedview.setModel(model)
        self.name.setText("")
        self.qty.setValue(0.0)
        self.start_date.setDateTime(QDateTime.currentDateTime())
        self.end_date.setDateTime(QDateTime.currentDateTime())
        self.animals.setModel(ListModel(FarmDB.instance().get_animals()))
        self.animals.setCurrentIndex(-1)
        self.supplies.setModel(ListModel(FarmDB.instance().get_supplies()))
        self.supplies.setCurrentIndex(-1)
        self.fq.setModel(ListModel([DropDownObj("daily",1),
                                    DropDownObj("biweekly", 2/7),
                                    DropDownObj("weekly", 1/7),
                                    DropDownObj("bimonthly", 2/28),
                                    DropDownObj("monthly", 1/28),
                                    DropDownObj("yearly", 1/365),
                                ]))
        self.fq.setCurrentIndex(-1)

    def add_sched(self):
        a_i = self.animals.currentIndex()
        s_i = self.supplies.currentIndex()
        f_i = self.fq.currentIndex()
        self.schedules = FarmDB.instance().add_schedule(
            self.name.text(),
            self.animals.model().currentObj(a_i),
            self.supplies.model().currentObj(s_i),
            self.qty.value(),
            self.fq.model().currentObj(f_i).value,
            self.start_date.date().toPython(),
            self.end_date.date().toPython(),
        )
        self.display()

    def show_units(self):
        s = self.supplies.model().currentObj(self.supplies.currentIndex())
        self.units.setText(str(s.units))
        self.notes.setText(str(s.notes))
        if(self.supplies.currentIndex() == -1):
            self.units.setText("")
            self.notes.setText("")


class DropDownObj():
    def __init__(self, name, value):
        self.name = name
        self.value = value
