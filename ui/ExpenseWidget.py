# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (QGroupBox, QFormLayout, QLabel, QLineEdit)
from PySide6.QtCore import Qt
from ui.Config import Config

class ExpenseWidget(QGroupBox):
    def __init__(self, main_window):
        QGroupBox.__init__(self, "  Add an Expenses")

        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Please enter expense information below:", alignment=Qt.AlignCenter))
        self.layout.addRow(QLabel("Cost"), QLineEdit())
        self.layout.addRow(QLabel("Type"), QLineEdit())
        self.layout.addRow(QLabel("Date"), QLineEdit())
        #self.layout.addRow(QLabel("Degree"), QComboBox())
        #self.layout.addRow(QLabel("Age"), QSpinBox())
        self.setLayout(self.layout)
