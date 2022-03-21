# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QInputDialog

class CreateFarmDialog(QInputDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Please create a farm")
        self.setCancelButtonText("Exit Farm Tool")
        self.setOkButtonText("Create Farm")
        self.setLabelText("Please enter the name of your farm: ")
        self.setTextValue("write farm name here")


