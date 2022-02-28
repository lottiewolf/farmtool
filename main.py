# This Python file uses the following encoding: utf-8
import sys
import os
import pandas as pd

from db.farm_db import Horse
from PySide6.QtCore import (QFile, QAbstractTableModel, Qt, QModelIndex)
from PySide6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QTableView)
from PySide6.QtWidgets import (QLabel, QPushButton)

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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Farm Tool 0.1")
        self.menubar = QMainWindow.menuBar(self)
        self.menubar.setObjectName("menubar")
        self.menu1 = self.menubar.addMenu("File")
        #self.menu1.add("Create Group")
        self.menu2 = self.menubar.addMenu("View")
        self.menu3 = self.menubar.addMenu("Help")


if __name__ == "__main__":
    app = QApplication([])

    farmview = QTableView()
    farmview.resize(500, 300)
    farmview.horizontalHeader().setStretchLastSection(True)
    farmview.setAlternatingRowColors(True)
    farmview.setSelectionBehavior(QTableView.SelectRows)
    try:
        df=pd.read_csv("data/farm2.csv")
        model = PandasModel(df)
        farmview.setModel(model)
        display = farmview
    except:
        text = QLabel("Welcome to FarmTool!", alignment=Qt.AlignCenter)
        button = QPushButton("Welcome to FarmTool!")
        display = text

    window = MainWindow()
    window.resize(800, 600)
    window.setCentralWidget(display)
    window.show()
    sys.exit(app.exec())
