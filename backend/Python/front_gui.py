import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import (Qt, QObject, QRect, pyqtSignal, QBasicTimer, QThread,
                          QMimeData)
from PyQt5.QtGui import QPixmap, QKeyEvent, QDrag, QPainter, QCursor
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QGridLayout, QVBoxLayout, QMainWindow,
                             QDialog, QFrame)

from gestor_archivos import ruta_banner_1

acceso_ventana, acceso_uic = uic.loadUiType("control_acceso.ui")


class VentanaAcceso(acceso_ventana, acceso_uic):
    signal_nombre_usuario = pyqtSignal(str)
    signal_iniciar_menu = pyqtSignal()

    def __init__(self, *args, **kwargs):
        # Inicializacion de Ventana
        super().__init__(*args, **kwargs)
        self.nombre_ventana = 'Control de Acceso - BigIA'
        self.setupUi(self)
        #self.setFixedSize(484, 654)  # Dimensión fija
        # Banner
        img_banner = QPixmap(ruta_banner_1)
        self.label_banner_1.setPixmap(img_banner)
        #self.label_banner_1.setMaximumHeight(300)
        self.label_banner_1.update()
        self.label_banner_1.show()
        # Conexión de botones y métodos de emisión de señal
        self.pb_entrar.clicked.connect(self.enviar_nombre)
        self.pb_salir.clicked.connect(self.cerrar_ventana)

    def mostrar_ventana(self):
        self.lineEdit_nombre.setText('')
        self.label_info_nombre.setText('')
        self.show()

    def cerrar_ventana(self):
        self.close()

    def enviar_nombre(self):
        nombre = self.lineEdit_nombre.text()
        self.signal_nombre_usuario.emit(nombre)

    def cambiar_info_texto(self, msg):
        self.label_info_nombre.setText(msg)

    def cambiar_color_texto(self, color):
        self.label_info_nombre.setStyleSheet(color)

    def iniciar_menu(self):
        self.hide()
        self.signal_iniciar_menu.emit()
