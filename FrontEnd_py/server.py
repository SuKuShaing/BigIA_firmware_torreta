import json
from flask import Flask, render_template  #render_template es para enviar html al navegador
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Rutas URLS
@app.route('/') #una ruta del objeto
def index():    #definimos una fc
    return render_template("index.html")    #envía un string

# @app.route('/about', strict_slashes=False)
# def about():
#     return render_template("about.html")

#Esta área es websocket
# Para mas información sobre websocket ir a https://flask-socketio.readthedocs.io/en/latest/getting_started.html
@socketio.on('coordAlServidor')
def fondo(coord):
    ##########################
    # Coordenadas X e Y aquí #
    ##########################
    # print(coord['posX'])
    # print(coord['posY'])
    socketio.emit('coordDelServidor', coord) #socketio.emit es en Broadcasting o Radiodifusión es decir se envía a todos los clientes conectados
@socketio.on('pyt')
def fuego():
    print("Fire!")
    #MAURO Aquí va a ir el comando que disparará
    emit('disparo', "Disparo ejecutado") #emit es solo entre el usuario y el servidor, independiente de cuantos hay conectados



if __name__ == '__main__':
    app.run(port = 1313, debug=True, host="0.0.0.0")  #app.run se encarga de ejecuar el servidor, por defecto en el puerto 5000, y el host por defecto es 127.0.0.1, La applicacion está en mododo de prueba, gracias a esta linea cada vez que cambio algo se reinicia el servidor
                                                        #los puertos 0 al 1024 están ocupados por el mismo pc, del 1025 al 65536 (2exp16)
