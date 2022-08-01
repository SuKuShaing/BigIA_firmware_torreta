import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QObject, QRect, pyqtSignal
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QGridLayout, QVBoxLayout, QMainWindow,
                             QDialog, QFrame)

from back_gui import Acceso

from front_gui import VentanaAcceso


if __name__ == "__main__":

    app = QApplication([])
    acceso = Acceso
    v_acceso = VentanaAcceso()
    v_acceso.show()
    v_acceso.signal_nombre_usuario.connect(acceso.control_usuario)
    #acceso.signal_mensaje_info_nombre.connect(v_acceso.cambiar_info_texto)
    #acceso.signal_color_info_nombre.connect(v_acceso.cambiar_color_texto)

    sys.exit(app.exec_())