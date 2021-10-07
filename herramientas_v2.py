# Importar librerias
import RPi.GPIO as GPIO
import time

# Setiar GPIO modo numeracion
GPIO.setmode(GPIO.BOARD)
freq = 53.5        # 53.5 Hz de pulso

# Configuracion de Pines 

GPIO.setup(7, GPIO.OUT)   # Salida Laser                                         
GPIO.setup(11, GPIO.OUT)  # Salida X
GPIO.setup(12, GPIO.OUT)  # Salida Y
GPIO.setup(13, GPIO.OUT)  # Salida D

GPIO.setup(15, GPIO.IN)   # Entrada Sensor Mov

def laser(estado):
    """Controla en on/off del laser"""
    if (estado == 1):
        GPIO.output(7, 1)
    elif (estado == 0):
        GPIO.output(7, 0)

def read_sensor_mov():
    """Detecta movimiento"""
    if GPIO.input(15):
        pass
    else:
        pass

class Servo():
    """Clase que modela el servo"""
    
    def __init__(self, pin, id):
        self.id = id
        self.pwm = GPIO.PWM(pin, freq)
        self.angulo = None
        self.pwm.start(0)

    def set_referencias(self, angulo_inicial):
        """Setea los angulos de referencia"""
        self.angulo_inicial = angulo_inicial
        
    def set_limites(self, min, max):
        """Setea los limites de movimiento del servo"""
        self.min = min
        self.max = max
    
    def inicio(self):
        """Mueve la posicion del servo a la de inicio"""
        self.mover_servo(self.angulo_inicial)
    
    def set_angulo(self, angulo):
        """Setea la posicion actual del servo"""    
        self.angulo = angulo

    def mover_servo(self, angulo):
        """Recibe un angulo y el servo a mover"""
        try:
            if ((angulo >= self.min) and (angulo <= self.max)):
                self.pwm.ChangeDutyCycle(2 + (angulo/18))
                time.sleep(0.02)
                self.pwm.ChangeDutyCycle(0)
                time.sleep(0.02)
                self.set_angulo(angulo)
            else:
                print("El servo {} intento moverse fuera de limite".format(id))
       
        except Exception as err:
            print("Error de tipo : {}".format(err))
