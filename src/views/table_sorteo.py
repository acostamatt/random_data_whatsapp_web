from models.table_sorteo import SorteoTableModel
from PySide6 import QtCore, QtWidgets
from views.base.table_view_sorteo import Ui_TableSorteo


class TableSorteo(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_TableSorteo()
        self.setup()

    def setup(self):
        self.ui.setupUi(self)
        self.ui.tableView.setStyleSheet("* { gridline-color: transparent }")
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignVCenter)
        self.__boton_exit = self.ui.buttonSalir

        self.__boton_exit.clicked.connect(self.clickedExitList)

    def set_sorteo_table_model(self, model):
        self.ui.tableView.setModel(model)

        self.header = self.ui.tableView.horizontalHeader()
        self.header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        model.refresh_data()

    def clickedExitList(self):
        self.deleteLater()
