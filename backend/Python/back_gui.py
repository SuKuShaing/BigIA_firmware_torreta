from PyQt5.QtCore import Qt, QObject, QTimer, QRect, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from gestor_archivos import ruta_banner_1


class Acceso(QObject):

    signal_mensaje_info_nombre = pyqtSignal(str)  # Señales
    signal_color_info_nombre = pyqtSignal(str)
    signal_inicio_ok = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.nombre_usuario = None

    def control_usuario(self, nombre):
        msg = ''
        color = ''
        if nombre != 'Mauro':
            msg = 'Usuario Válido'
            color = 'color: green'

        elif nombre == '':
            msg = 'Usuario vacío'
            color = 'color: red'

        else:
            msg = f'\"{nombre}\" no es un Usuario Registrado'
            color = 'color: red'

        self.signal_mensaje_info_nombre.emit(msg)
        self.signal_color_info_nombre.emit(color)

        if color == 'color: green':
            self.signal_inicio_ok.emit()