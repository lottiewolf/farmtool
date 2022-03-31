# This Python file uses the following encoding: utf-8

from PySide6.QtCore import (QAbstractListModel, Qt, QModelIndex)
import pandas as pd


class ListModel(QAbstractListModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, data, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the data
        """
        if parent == QModelIndex():
            return len(self._data)

        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return list of names from the data object
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return str(self._data[index.row()].name)

        return None

    def currentObj(self, i):
        return self._data[i]
