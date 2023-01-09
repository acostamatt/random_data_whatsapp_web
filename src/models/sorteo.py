import pymysql
import datetime

from config.env import *

class Sorteo:
    def __init__(self):
        self.DB_HOST = DB_HOST
        self.DB_USER = DB_USER
        self.DB_NAME = DB_NAME
        self.WHATSAPP_USER = WHATSAPP_USER
        self.WORD_SEARCH = WORD_SEARCH

        try:
            self.conn = pymysql.connect(host=self.DB_HOST,
                                    user=self.DB_USER,
                                    password='',
                                    db=self.DB_NAME)
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
	        print("Ocurrió un error al conectar: ", e)

    def insertMensaje(self, contacto, mensaje, fecha):
        with self.conn.cursor() as cursor:
            insert = "INSERT INTO mensajes(contacto, mensaje, fecha) VALUES (%s, %s, %s);"
            fecha = datetime.datetime.strptime(fecha, "%d/%m/%Y %H:%M")

            cursor.execute(insert, (contacto, mensaje, fecha))
        self.conn.commit()

    def insertSorteo(self, id_mensaje, fecha_desde, fecha_hasta):
        with self.conn.cursor() as cursor:
            insert = "INSERT INTO sorteos(id_mensaje, fecha_desde, fecha_hasta, fecha_sorteo) VALUES (%s, %s, %s, %s);"

            cursor.execute(insert, (id_mensaje, fecha_desde, fecha_hasta, self.getTodayDate()))
        self.conn.commit()

    def checkSavedMessage(self, contacto, mensaje, fecha):
        with self.conn.cursor() as cursor:
			
            select = "SELECT id FROM mensajes WHERE contacto = %s AND mensaje = %s AND fecha = %s;"
            fecha = datetime.datetime.strptime(fecha, "%d/%m/%Y %H:%M")
            cursor.execute(select, (contacto, mensaje, fecha))

            # Con fetchall traemos todas las filas
            return len(cursor.fetchall())

    def checkSavedDraw(self, id_mensaje):
        with self.conn.cursor() as cursor:
			
            select = "SELECT id FROM sorteos WHERE id_mensaje = %s;"
            cursor.execute(select, (id_mensaje))

            # Con fetchall traemos todas las filas
            return len(cursor.fetchall())

    def generateDraw(self, fecha_desde, fecha_hasta):
        with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
            select = "SELECT * FROM mensajes WHERE fecha BETWEEN %s AND %s ORDER BY rand() LIMIT 1;"
            cursor.execute(select, (fecha_desde, fecha_hasta))

            mensaje_sorteo = cursor.fetchone()
            if not self.checkSavedDraw(mensaje_sorteo['id']):
                self.insertSorteo(mensaje_sorteo['id'], fecha_desde, fecha_hasta)
                return mensaje_sorteo
            else:
                return 'No se encontraron coincidencias.'
        
    def getTodayDate(self):
        fecha_str = datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y %H:%M")
        return datetime.datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")