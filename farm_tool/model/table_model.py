# This Python file uses the following encoding: utf-8

from PySide6.QtCore import (QAbstractTableModel, Qt, QModelIndex)
from farm_tool.controller.farm import Farm
import pandas as pd


class TableModel(QAbstractTableModel):

    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data
        try:
            self._h_header = self._data[0].header()
        except:
            # for the report, where there is no table obj with .header()
            self._h_header = [""]*len(self._data[0])
        self._v_header = [""]*len(self._data)

    def rowCount(self, parent=QModelIndex()) -> int:
        if parent == QModelIndex():
            return len(self._data)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        if self.rowCount() == 0:
            return 0

        if parent == QModelIndex():
            return len(self._h_header)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        if self.rowCount() == 0:
            return None

        if not index.isValid():
            return None

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return str(self._data[index.row()][index.column()])
        return None

    def setData(self, index, value, role):
            if role == Qt.EditRole:
                new_obj = Farm.instance().edit(self._data[index.row()], index.column(), value)
                self._data[index.row()] = new_obj
                return True

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        if self.rowCount() == 0:
            return None

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.display_hdr(str(self._h_header[section]))
            elif orientation == Qt.Vertical:
                if self._v_header[section] == "":
                    return str(section+1)
                else:
                    return self._v_header[section]
        return None

    def setHeaderData(self, section: int, orientation: Qt.Orientation, value):
        if orientation == Qt.Horizontal:
            self._h_header[section] = value
        elif orientation == Qt.Vertical:
            self._v_header[section] = value
        return True

    def display_hdr(self, str):
        parts = str.split("_")
        capitalized_parts = [p.capitalize() for p in parts]
        disply_str = " ".join(capitalized_parts)
        return disply_str

    def flags(self, index):
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable
