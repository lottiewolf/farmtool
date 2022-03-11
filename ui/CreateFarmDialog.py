# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class CreateFarmDialog(QInputDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Please create a farm")
        self.setCancelButtonText("Exit Farm Tool")
        self.setOkButtonText("Create Farm")
        self.setLabelText("Please enter the name of your farm: ")
        self.setTextValue("write farm name here")

        #QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        #self.buttonBox = QDialogButtonBox(QBtn)
        #self.buttonBox.accepted.connect(self.accept)
        #self.buttonBox.rejected.connect(self.reject)

        self.layout = QFormLayout()
        message = QLabel("Welcome to FarmTool!")
        self.layout.addWidget(message)
        self.layout.addRow(QLabel("Please enter the name of your farm: ", alignment=Qt.AlignRight), QLineEdit())
        self.layout.addRow(QLabel("Please enter a working directory:", alignment=Qt.AlignRight), QLineEdit())
        #self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
