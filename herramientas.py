# Importar librerias
import RPi.GPIO as GPIO
import time


# Setiar GPIO modo numeracion
GPIO.setmode(GPIO.BOARD)
freq = 53.5        # 53.5 Hz de pulso


# Configuracion de Pines
GPIO.setup(11, GPIO.OUT)  # Para X
GPIO.setup(12, GPIO.OUT)  # Para Y
GPIO.setup(13, GPIO.OUT)  # Para D

class Servo():
    """Clase que modela el servo"""
    
    def __init__(self, pin):
        self.pwm = GPIO.PWM(pin, freq)
        self.angulo = None
        self.pwm.start(0)

def set_angulo(servo, angulo):
    """Setea la posicion inicial del servo"""    
    servo.angulo = angulo


def set_limites(servo, min, max):
    """Setea los limites de movimiento del servo"""
    servo.min = min
    servo.max = max


def mover_servo(servo, angulo):
    """Recibe un angulo y el servo a mover"""
    try:
        if ((angulo >= servo.min) and (angulo <= servo.max)):
            servo.pwm.ChangeDutyCycle(2 + (angulo/18))
            time.sleep(0.02)
            servo.pwm.ChangeDutyCycle(0)
            time.sleep(0.02)
            set_angulo(servo, angulo)
   
    except Exception as err:
        print("Error de tipo : {}".format(err))
    
    
def reset(servo):
    """Resetea la posicion inicial del servo"""
    mover_servo(servo.inicial, servo)
