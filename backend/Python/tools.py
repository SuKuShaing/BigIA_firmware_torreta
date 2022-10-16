import time
from time import sleep
import RPi.GPIO as GPIO


class Stepper():
    """Clase que modela los stepper"""

    def __init__(self, nombre, id):
        self.nombre = nombre
        self.angulo = None
        self.id = id
        self.ROT = 1 # default CW
        self.delay = 0.0000608 / 32

        if id == 1:
            self.DIR = 20
            self.STEP = 21

        elif id == 2:
            self.DIR = 19
            self.STEP = 26
            
    def mover_stepper(self, sentido, pasos):

        if sentido == 'CW':
            self.ROT = 1
            print(" {}, DIR : {}, ROT : {}".format(self.nombre, self.DIR, self.ROT))
            GPIO.output(self.DIR, 1)
        elif sentido == 'CCW':
            self.ROT = 0
            print(" {}, DIR : {}, ROT : {}".format(self.nombre, self.DIR, self.ROT))
            GPIO.output(self.DIR, 0)
        
        for x in range(pasos):
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(self.delay)
