from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QDateTime

from controllers.sorteo import SorteoController
from models.table_sorteo import SorteoTableModel
from views.base.sorteo_base import Ui_Form
from views.table_sorteo import TableSorteo


class Sorteo(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Form()
        self.sorteo_controller = SorteoController()

        self.setup()

    def setup(self):
        self.ui.setupUi(self)
        self.__fecha_desde = self.ui.fechaDesde
        self.__fecha_hasta = self.ui.fechaHasta
        self.__boton_obtener_datos = self.ui.botonObtenerDatos
        self.__boton_sorteo = self.ui.botonSortear
        self.__boton_listar_ganadores = self.ui.botonListarSorteos

        self.set_date_previous_days(self.__fecha_desde)
        self.set_date_today(self.__fecha_hasta)
        self.set_maximum_height_view(165)

        self.__boton_obtener_datos.clicked.connect(self.obtener_datos)
        self.__boton_sorteo.clicked.connect(self.on_enviar_datos_sorteo)
        self.__boton_listar_ganadores.clicked.connect(self.listar_ganadores)

    def obtener_datos(self):
        self.sorteo_controller.execute()
        self.set_maximum_height_view(165)
        msj_label = f"<div style='color:#008F39'><strong>Datos obtenidos correctamente</strong></div>"

        self.ui.labelSorteo.setText(msj_label)

    def on_enviar_datos_sorteo(self):
        data_sorteo = self.sorteo_controller.get_draw(
            self.__fecha_desde.text(), self.__fecha_hasta.text()
        )
        self.set_data_sorteo(data_sorteo)

    def set_data_sorteo(self, data):
        try:
            contacto = data["contacto"]
            mensaje = data["mensaje"]
            fecha = data["fecha"]
            msj_label = f"<div style='color:#008F39'><strong>{contacto}</strong></div><div><p>{mensaje}</p></div><div><p>{fecha}</p></div>"
            self.set_maximum_height_view(300)

        except:
            msj_label = f"<div style='color:#FF0000'><strong>{data}</strong></div>"
            self.set_maximum_height_view(165)

        self.ui.labelSorteo.setText(msj_label)

    def listar_ganadores(self):
        self.__table_sorteo = TableSorteo()
        self.__table_model_sorteo = SorteoTableModel()
        self.__table_sorteo.set_sorteo_table_model(self.__table_model_sorteo)
        self.__table_sorteo.setFixedWidth(1500)
        self.__table_sorteo.show()

    def set_date_today(self, date_time_widget: QDateTime):
        date_time_widget.setDateTime(QtCore.QDateTime.currentDateTime())

    def set_date_previous_days(self, date_time_widget: QDateTime):
        fecha_desde = QtCore.QDateTime.addDays(QtCore.QDateTime.currentDateTime(), -7)
        date_time_widget.setDateTime(fecha_desde)

    def set_maximum_height_view(self, int_height):
        self.setFixedHeight(int_height)
        self.ui.labelSorteo.setText("")
