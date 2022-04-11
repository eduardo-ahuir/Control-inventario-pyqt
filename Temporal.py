import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QListWidgetItem
)

fichero_interfaz = "./inventario.ui"

inventario_ui, QtBaseClass = uic.loadUiType(fichero_interfaz)

bbdd = "inventarioclase.bd"
tabla = "almacen"


class baseDatos():

    def iniciar(self):
        self.con = sqlite3.connect(bbdd)
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + tabla + " (producto TEXT,existencias TEXT, precio TEXT)")
        self.con.commit()

    def consulta(self, cadena):
        self.cursor.execute(cadena)
        self.con.commit()
        return self.cursor.fetchall()

    def Borrar(self, elemento):
        self.cursor.execute("DELETE FROM " + tabla + " WHERE PRODUCTO = '" + elemento + "'")
        self.con.commit()

    def introducir(self, registro):
        self.cursor.execute("INSERT INTO " + tabla + " VALUES (?,?,?)", registro)
        self.con.commit()
        print("Prueba")

    def cerrar(self):
        self.con.close()


class MainWindow(QMainWindow, inventario_ui):

    def __init__(self):
        QMainWindow.__init__(self)
        inventario_ui.__init__(self)
        self.setupUi(self)
        self.base = baseDatos()
        self.base.iniciar()
        self.conexionSenales()
        self.mostrar()

    def limpiar(self):
        self.producto.clear()
        self.unidades.clear()
        self.precio.clear()

    def anadir(self):
        registro = (self.producto.text(), self.unidades.text(), self.precio.text())
        self.base.introducir(registro)
        self.listaProductos.addItem(self.producto.text())
        self.limpiar()

    def borrar(self):
        elemento = self.listaProductos.currentItem().text()
        cborrar = self.listaProductos.currentRow()
        print(cborrar)
        self.listaProductos.takeItem(cborrar)
        self.base.Borrar(elemento)
        print("Borrado")
        self.limpiar()

    def editar(self):
        self.base.consulta("UPDATE "+tabla+" SET producto='"+self.producto.text()+"' WHERE producto = '"+self.listaProductos.currentItem().text()+ "'")
        self.base.consulta("UPDATE " + tabla + " SET existencias='" + self.unidades.text() + "' WHERE producto = '" + self.listaProductos.currentItem().text() + "'")
        self.base.consulta("UPDATE " + tabla + " SET precio='" + self.precio.text() + "' WHERE producto = '" + self.listaProductos.currentItem().text() + "'")
        print(self.unidades.text())
        self.limpiar()
        self.mostrar()
        print("Edicion hecha")


    def buscar(self):
        datos = self.base.consulta("SELECT * FROM almacen WHERE producto= '" + self.listaProductos.currentItem().text() + "'")
        for i in range(len(datos)):
            self.producto.setText(datos[0][0])
            self.unidades.setText(datos[0][1])
            self.precio.setText(datos[0][2])

    def mostrar(self):
        datos = self.base.consulta("SELECT * FROM " + tabla)
        self.listaProductos.clear()
        for i in range(len(datos)):
            item = QListWidgetItem(str(datos[i][0]))
            self.listaProductos.insertItem(i, item)
            self.limpiar()
    def pruebas(self):
        print("hola")

    def conexionSenales(self):
        self.btnanadir.pressed.connect(self.anadir)
        self.eliminar.pressed.connect(self.borrar)
        self.busqueda.pressed.connect(self.buscar)
        self.btneditar.pressed.connect(self.editar)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
