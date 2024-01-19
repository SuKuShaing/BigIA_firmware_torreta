from flask import Flask, render_template  #render_template es para enviar html al navegador
from flask_socketio import SocketIO, emit

import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) #permite ejecutar este server como si fuese raíz
sys.path.append(PROJECT_ROOT)
# import backend.Python.torreta_v05_funcional as tf
#Más información sobre como importar bien en https://towardsdatascience.com/understanding-python-imports-init-py-and-pythonpath-once-and-for-all-4c5249ab6355
import torr_v2_web as tf


app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# Rutas URLS
@app.route('/') #una ruta del objeto
def index():    #definimos una fc
    return render_template("index.html")  #envía un string


# @app.route('/about', strict_slashes=False)
# def about():
#     return render_template("about.html")


# Esta área es websocket
# Seba sacaste información sobre websocket en https://flask-socketio.readthedocs.io/en/latest/getting_started.html
@socketio.on('mover_torreta')
def mover(coord):
    if coord['posY'] == -1:
        tf.mov_abajo()
    if coord['posY'] == 1:
        tf.mov_arriba()
    if coord['posX'] == 1:
        tf.mov_derecha()
    if coord['posX'] == -1:
        tf.mov_izquierda()


@socketio.on('coordAlServidor')
def fondo(coord):
    #Cuando se logre conectar la cámara, borrar esta función
    print("posX", coord['posX'])
    print("posY", coord['posY'])
    socketio.emit('coordDelServidor', coord) #socketio.emit es en Broadcasting o Radiodifusión es decir se envía a todos los clientes conectados


@socketio.on('aumentos')
def aumento(au):
    if au['autm'] == 'Aumentar':
        tf.aum_vel_mov()
    if au['autm'] == 'Disminuir':
        tf.dis_vel_mov()


@socketio.on('pyt')
def fuego():
    print("¡Fire!")
    tf.disparar()
    emit('disparo', "Disparo ejecutado") #emit es solo entre el usuario y el servidor, independiente de cuantos hay conectados



##############################################################
##################### Zona de Debugging ######################
##############################################################


##################### Zona de Debugging ######################

@app.route('/debug')
def debug():
    return render_template("debug.html")


@socketio.on('tiempoPaso')
def mover_debug(data):
    print(f"En el server data['pasos']: {data['pasos']} y data['tiempoHigh']: {data['tiempoHigh']}")
    tf.mov_izquierda_prueba(data['pasos'], data['tiempoHigh'])


##############################################################
##################### Zona de ejecución ######################
##############################################################

if __name__ == '__main__':
    app.run(port = 1313, debug=False, host="0.0.0.0")  #app.run se encarga de ejecutar el servidor, por defecto en el puerto 5000, y el host por defecto es 127.0.0.1, La aplicación está en modo de prueba, gracias a esta linea cada vez que cambio algo se reinicia el servidor
    # app.run(port = 1313)  #app.run se encarga de ejecutar el servidor, por defecto en el puerto 5000, y el host por defecto es 127.0.0.1, La aplicación está en modo de prueba, gracias a esta linea cada vez que cambio algo se reinicia el servidor
                                                        #los puertos 0 al 1024 están ocupados por el mismo pc, del 1025 al 65536 (2exp16)
# flask
# flask_socketio