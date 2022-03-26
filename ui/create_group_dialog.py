# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QInputDialog

class CreateGroupDialog(QInputDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Please create a group")
        self.setCancelButtonText("Cancel")
        self.setOkButtonText("Create Group")
        self.setLabelText("Please enter the name of your group: ")
        self.setTextValue("my barn name")
