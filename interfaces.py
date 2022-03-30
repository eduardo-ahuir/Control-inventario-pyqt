import sqlite3, sys
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import (
    QApplication, QMessageBox, QMainWindow, QListWidgetItem
)

fichero_interfaz = "inventario.ui"
Prueba, QtBaseClass = uic.loadUiType(fichero_interfaz)

bbdd = "inventario.bd"
tabla = "almacen"


class baseDatos():
    def iniciar(self):
        self.con = sqlite3.connect(bbdd)
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + tabla + " (producto TEXT,existencias TEXT, precio TEXT)")
        self.con.commit()

    def introducir(self, registro):
        self.cursor.execute("INSERT INTO " + tabla + " VALUES (?,?,?)", registro)
        self.con.commit()


class Ventana(QMainWindow, Prueba):

    def __init__(self):
        QMainWindow.__init__(self)
        Prueba.__init__(self)
        self.setupUi(self)
        bd = baseDatos()
        bd.iniciar()
        self.conexionSenales()

    def conexionSenales(self):
        bd = baseDatos()
        self.anadir.pressed.connect(bd.introducir(bd))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Ventana()
    gui.show()
    app.exec_()
