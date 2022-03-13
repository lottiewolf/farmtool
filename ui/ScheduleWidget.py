# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (QGroupBox, QFormLayout, QLabel, QLineEdit, QComboBox, QSpinBox)
from PySide6.QtCore import Qt
from ui.Config import Config

class ScheduleWidget(QGroupBox):
    def __init__(self, main_window):
        QGroupBox.__init__(self, "  Add a Schedule")

        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Please enter a daily schedule below:", alignment=Qt.AlignCenter))
        self.layout.addRow(QLabel("Name of Animal"), QLineEdit())
        self.layout.addRow(QLabel("Supply"), QComboBox())
        self.layout.addRow(QLabel("Date"), QSpinBox())
        self.setLayout(self.layout)
