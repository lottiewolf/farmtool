#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 13:52:49 2022

@author: cwolf
"""
import PySide6.QtCore
import pandas as pd

#from PyQt5 import QtGui, QtWidgets
import sys
import locale
import logging
import logging.handlers
import time
import os
import os.path
#import ui.views
#from ui.views.main import MainWindow
#from ui.splash.splash_screens import SplashScreen
#from ui.views import swap_ui_content
#from ui.views.basic_consumption_views import BasicConsumptionPanelWidget
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QTableWidget,
                               QTableWidgetItem, QTableView)
from PySide6.QtCore import (QAbstractTableModel, Qt, QModelIndex)

logging.basicConfig()
colors = [("Red", "#FF0000"),
          ("Green", "#00FF00"),
          ("Blue", "#0000FF"),
          ("Black", "#000000"),
          ("White", "#FFFFFF"),
          ("Electric Green", "#41CD52"),
          ("Dark Blue", "#222840"),
          ("Yellow", "#F9E56d")]


class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])

        return None


#class MainWindow(QtWidgets.QWidget):
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Farm Tool 0.1")
        self.centralwidget = self.centralWidget()
        self.menubar = QtWidgets.QMainWindow.menuBar(self)
        self.menubar.setObjectName("menubar")
        self.menu1 = self.menubar.addMenu("File")
        self.menu2 = self.menubar.addMenu("View")
        self.menu3 = self.menubar.addMenu("Help")
        
        #self.centralwidget.
       
        #self.menuFile.setObjectName("menuFile")
        #self.menu = QtWidgets.QMenu()
        
        #def createMenus(self):
        #    fileMenu = menuBar().addMenu(tr("File"))
        #    fileMenu.addAction(newAct)
        #    fileMenu.addAction(openAct)
        #    fileMenu.addAction(saveAct)
        
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Welcome to BarnTool!", alignment=QtCore.Qt.AlignCenter)
        self.edit = QtWidgets.QLineEdit("Write my name here..")
        
        #self.layout = QtWidgets.QVBoxLayout(self)
        #self.layout.addWidget(self.text)
        #self.layout.addWidget(self.edit)
        #self.layout.addWidget(self.button)
        #self.layout.addWidget(self.menu)
       
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 29))
        
        #self.menuFile = QtWidgets.QMenu(self.menubar)
        #self.menuFile.setObjectName("menuFile")
        #self.menuAnalysis = QtWidgets.QMenu(self.menubar)
        #self.menuAnalysis.setObjectName("menuAnalysis")
        #self.menuView = QtWidgets.QMenu(self.menubar)
        #self.menuView.setObjectName("menuView")
        #self.menuHelp = QtWidgets.QMenu(self.menubar)
        #self.menuHelp.setObjectName("menuHelp")
       

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))


if __name__ == "__main__":
    # app = QtWidgets.QApplication([]) #sys.argv)
    app = QtWidgets.QApplication.instance()
    if app == None:
        app = QtWidgets.QApplication([])

    def get_rgb_from_hex(code):
        code_hex = code.replace("#", "")
        rgb = tuple(int(code_hex[i:i+2], 16) for i in (0, 2, 4))
        return QColor.fromRgb(rgb[0], rgb[1], rgb[2])

    table = QTableWidget()
    table.setRowCount(len(colors))
    table.setColumnCount(len(colors[0]) + 1)
    table.setHorizontalHeaderLabels(["Name", "Hex Code", "Color"])

    for i, (name, code) in enumerate(colors):
        item_name = QTableWidgetItem(name)
        item_code = QTableWidgetItem(code)
        item_color = QTableWidgetItem()
        item_color.setBackground(get_rgb_from_hex(code))
        table.setItem(i, 0, item_name)
        table.setItem(i, 1, item_code)
        table.setItem(i, 2, item_color)

    df=pd.read_csv("my_csv.csv")
    model = PandasModel(df)
    farmview = QTableView()
    farmview.resize(500, 300)
    farmview.horizontalHeader().setStretchLastSection(True)
    farmview.setAlternatingRowColors(True)
    farmview.setSelectionBehavior(QTableView.SelectRows)
    farmview.setModel(model)
    #view.show()

    window = MainWindow()
    window.resize(800, 600)
    window.setCentralWidget(farmview)
    window.show()
    #table.show()
    # window.showMaximized()

    sys.exit(app.exec())


def check_user_folder():
    folder_path = os.path.join(os.path.expanduser("~"), ".barntool")
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

# if __name__ == "__main__":

#    check_user_folder()
#    configure_logging()
#    locale.setlocale(locale.LC_ALL, '')

#    app = QtWidgets.QApplication(sys.argv)
#    splash = create_splash()
#    start = time.time()
#    splash.show()

#    while time.time() - start < 2:
#        time.sleep(0.001)
#        app.processEvents()
#    window = MainWindow()

#    ui.views.register_main_window(window)

#    import db
#    init_db()

    # load the basic consumption panel as default view
#    swap_ui_content(BasicConsumptionPanelWidget)

#    splash.hide()
#    splash.close()
