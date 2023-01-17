import datetime

from models.sorteo import Sorteo
from PySide6 import QtCore
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QSize, Qt


class SorteoTableModel(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)
        self.headers = [
            "Contacto",
            "Mensaje",
            "Fecha Mensaje",
            "Fecha Desde",
            "Fecha Hasta",
            "Fecha Sorteo",
        ]
        self.headers_widths = [150, 750, 150, 150, 150, 150]
        self.sorteos = []

    def refresh_data(self):
        self.sorteos = Sorteo().listSorteos()
        self.modelReset.emit()

    def rowCount(self, parent=None):
        return len(self.sorteos)

    def columnCount(self, parent=None):
        return len(self.headers)

    def getFormarDateStr(self, date_origin):
        date_str = datetime.datetime.strftime(date_origin, "%Y-%m-%d %H:%M")
        return date_str

    def data(self, index: QModelIndex, role=None):
        sorteo = self.sorteos[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return sorteo["contacto"]

            if index.column() == 1:
                return sorteo["mensaje"]

            if index.column() == 2:
                return self.getFormarDateStr(sorteo["fecha_mensaje"])

            if index.column() == 3:
                return self.getFormarDateStr(sorteo["fecha_desde"])

            if index.column() == 4:
                return self.getFormarDateStr(sorteo["fecha_hasta"])

            if index.column() == 5:
                return self.getFormarDateStr(sorteo["fecha_sorteo"])

        if role == Qt.UserRole:
            return sorteo["id"]

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self.headers[section]

            if role == Qt.SizeHintRole:
                return QSize(self.headers_widths[section], 23)
