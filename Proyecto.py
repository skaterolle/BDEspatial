import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
# from pyqtlet2 import L, MapWidget
from pyqtlet import L, MapWidget
import pyproj
from pathlib import Path


# Necesario para el funcionamiento
# - PyQT5
# - pyqtlet
# - pyproj
class MapWindow(QWidget):

    def __init__(self):

        # Setting up the widgets and layout
        super(MapWindow, self).__init__()
        # Creación del MapWidget para el funcionamiento de qytlet
        self.mapWidget = MapWidget()
        self.mapWidget.setObjectName("Mapa")

        # # Working with the maps with pyqtlet
        self.map = L.map(self.mapWidget)
        self.map.setView([37.2739, -6.9390], 10)
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(self.map)

        # Llamada a la función que genera la ventana
        self.initUI()
    # Función ejecutada cada vez que se clica el botón

    def button_clicked(self):
        global splitter1, datos, marcador
        # Transformar las entradas del txt a EPSG:32630 con pyproj 2
        proj = pyproj.Transformer.from_crs(32630, 4326, always_xy=True)
        if marcador:
            for x in range(len(marcador)):
                self.map.removeLayer(marcador[x])
        marcador = []

        suceso = splitter1.Sucesos.currentText()
        año = splitter1.Anos.currentText()
        for x in range(len(datos)):
            x1, y1 = (datos[x][0], datos[x][1])
            x2, y2 = proj.transform(x1, y1)
            if datos[x][2] == año and datos[x][3] == suceso:
                pop = datos[x][2] + " - " + datos[x][3]
                self.marker = L.marker([y2, x2])
                marcador.append(self.marker)
                self.marker.bindPopup(pop)
                self.map.addLayer(self.marker)
                # print(datos[x])
            elif datos[x][2] == año and suceso == "No Filtrar":
                pop = datos[x][2] + " - " + datos[x][3]
                self.marker = L.marker([y2, x2])
                marcador.append(self.marker)
                self.marker.bindPopup(pop)
                self.map.addLayer(self.marker)
                # print(datos[x])
            elif datos[x][3] == suceso and año == "No Filtrar":
                pop = datos[x][2] + " - " + datos[x][3]
                self.marker = L.marker([y2, x2])
                marcador.append(self.marker)
                self.marker.bindPopup(pop)
                self.map.addLayer(self.marker)
                # print(datos[x])
            # else:
                #print("No hay casos")
        # print(suceso)
        # print(año)
        # print("clicked")

    def initUI(self):
        # Declaración de datos globales
        global splitter1, datos, marcador
        marcador = []
        datos = load_datas()

        # Busqueda de los sucesos dentro de la variable datos
        actos = []
        for x in range(len(datos)):
            actos.append(datos[x][3])
        lista_final = list(dict.fromkeys(actos))
        # print(lista_final)

        # Busqueda de los años dentro de la variable datos
        actos = []
        for x in range(len(datos)):
            actos.append(datos[x][2])
        años = list(dict.fromkeys(actos))
        años.sort()

        hbox = QHBoxLayout(self)

        # Inicialización del Splitter1 para mostrar el buscador
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.setSizes([100, 200])

        splitter1.label = QtWidgets.QLabel(splitter1)
        splitter1.label.setGeometry(QtCore.QRect(420, 490, 47, 13))
        splitter1.label.setObjectName("label")

        # Creación del comboBox de los sucesos y agregación de sus componentes
        splitter1.Sucesos = QtWidgets.QComboBox(splitter1)
        splitter1.Sucesos.setGeometry(QtCore.QRect(20, 490, 141, 22))
        splitter1.Sucesos.setObjectName("Sucesos")
        splitter1.Sucesos.addItem("No Filtrar")
        for x in range(len(lista_final)):
            splitter1.Sucesos.addItem(lista_final[x])

        splitter1.label2 = QtWidgets.QLabel(splitter1)
        splitter1.label2.setGeometry(QtCore.QRect(420, 490, 47, 13))
        splitter1.label2.setObjectName("label2")

        # Creación del comboBox de los Años y agregación de sus componentes
        splitter1.Anos = QtWidgets.QComboBox(splitter1)
        splitter1.Anos.setGeometry(QtCore.QRect(160, 490, 141, 22))
        splitter1.Anos.setObjectName("Anos")
        splitter1.Anos.addItem("No Filtrar")
        for x in range(len(años)):
            splitter1.Anos.addItem(años[x])

        # Creación del botón de recarga
        splitter1.Reload = QtWidgets.QPushButton(splitter1)
        splitter1.Reload.setGeometry(QtCore.QRect(310, 490, 75, 23))
        splitter1.Reload.setObjectName("Reload")
        splitter1.Reload.clicked.connect(self.button_clicked)

        # Creación del segundo Splitter donde estará el mapa
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.mapWidget)

        hbox.addWidget(splitter2)
        self.retranslateUi(MapWindow)
        self.setLayout(hbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

        # Establecemos el tamaño y la posición de la ventana
        self.setGeometry(800, 200, 800, 600)
        self.setWindowTitle('QSplitter demo')
        self.show()

    # Inicializamos los labels
    def retranslateUi(self, MainWindow):
        global splitter1
        _translate = QtCore.QCoreApplication.translate
        splitter1.label.setText(_translate("MapWindow", "Tipo de Suceso:"))
        splitter1.label2.setText(_translate("MapWindow", "Año:"))
        splitter1.Reload.setText(_translate("MainWindow", "Recargar"))

# Definición de función para la carga de los datos desde el archivo .txt


def load_datas():
    f = open("./sucesosHuelva.txt", "r")
    lista = []
    while True:
        line = f.readline()
        if not line:
            break
        if line[0] != '@':
            tipo = [str(x) for x in line.split()]
            # print(''.join(tipo))
            lista.append(tipo)
    f.close()
    return lista


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MapWindow()
    # widget.show()
    sys.exit(app.exec_())
    # load_datas_tipo()
