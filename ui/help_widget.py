# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (QDockWidget, QListWidget)
from PySide6.QtCore import Qt

class HelpWidget(QDockWidget):
    def __init__(self, main_window):
        QDockWidget.__init__(self, "Help Window", main_window)

        self.listWidget = QListWidget()
        self.listWidget.addItem("item1")
        self.listWidget.addItem("item2")
        self.listWidget.addItem("item3")
        self.setWidget(self.listWidget)
        self.setFloating(False)

        #dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        #dockWidget.setWidget(dockWidgetContents)
        #addDockWidget(Qt.LeftDockWidgetArea, dockWidget)
