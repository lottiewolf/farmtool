# This Python file uses the following encoding: utf-8

from PySide6.QtCore import (QAbstractTableModel, Qt, QModelIndex)
import pandas as pd


class TableModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._data)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if self.rowCount() == 0:
            return 0

        if parent == QModelIndex():
            return len(self._data[0].header())
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if self.rowCount() == 0:
            return None

        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            #return str(self._data.iloc[index.row(), index.column()]
            return str(self._data[index.row()][index.column()])

        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if self.rowCount() == 0:
            return None

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data[0].header()[section])

        return None
