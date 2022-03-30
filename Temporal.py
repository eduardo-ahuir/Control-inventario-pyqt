import sqlite3, sys


from PyQt5 import QtGui, uic


from PyQt5.QtWidgets import(
 QApplication, QMessageBox, QMainWindow, QListWidgetItem
)

fichero_interfaz = "./inventario.ui"

inventario_ui, QtBaseClass = uic.loadUiType(fichero_interfaz)


bbdd="inventarioclase.bd"
tabla="almacen"

class baseDatos():
    
    def iniciar(self):
        self.con=sqlite3.connect(bbdd)
        self.cursor=self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS "+tabla+" (producto TEXT,existencias TEXT, precio TEXT)")
        self.con.commit()
    
    def consulta(self,cadena):
        self.cursor.execute(cadena)
        self.con.commit()
        return self.cursor.fetchall()
 
    def eliminar(self,elemento):
        self.cursor.execute("DELETE FROM "+tabla+" WHERE PRODUCTO = '"+elemento+"'")
        self.con.commit
    
    def introducir(self,registro):
        self.cursor.execute("INSERT INTO "+tabla+" VALUES (?,?,?)", registro)
        self.con.commit()
        print("Prueba")
 
    def cerrar(self):
        self.con.close()

class MainWindow(QMainWindow, inventario_ui):
    
    def __init__(self):
        QMainWindow.__init__(self)
        inventario_ui.__init__(self)
        self.setupUi(self)
        self.base=baseDatos()
        self.base.iniciar()
        self.conexionSenales()
        self.mostrar()
        
        
    def anadir(self):
        registro=(self.producto.text(),self.unidades.text(),self.precio.text())
        self.base.introducir(registro)
    #def eliminar(self):
 
    def editar(self):
        self.base.consulta("UPDATE "+tabla+" SET existencias="+self.unidadesEdit.text()+"WHERE producto='"+self.listaProductos.currentItem().text()+"'")
        self.base.consulta("UPDATE "+tabla+" SET precio="+self.precioEdit.text()+" WHERE producto='"+self.listaProductos.currentItem().text()+"'")
 
    #def buscar(self):
    
    def mostrar(self):
        datos=self.base.consulta("SELECT * FROM "+tabla)
        for i in range(len(datos)):
            item = QListWidgetItem(datos[i][:])
            self.listaProductos.insertItem(i, item)

    def conexionSenales(self):
        
        self.btnanadir.pressed.connect(self.anadir)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()