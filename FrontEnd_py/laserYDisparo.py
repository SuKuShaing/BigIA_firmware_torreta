import RPi.GPIO as GPIO
from time import sleep

# Pines
SHOT = 25
LASER = 100 # colocar el pin real del láser aquí

GPIO.setup(SHOT, GPIO.OUT)
GPIO.setup(LASER, GPIO.OUT)


# Esto se puede colocar en otra hoja
def disparar():
    GPIO.output(SHOT, 1)
    sleep(0.1)
    GPIO.output(SHOT, 0)
    print("Disparé")


def prender_laser():
    GPIO.output(LASER, 1)
    print("Prendí el láser")


def apagar_laser():
    GPIO.output(LASER, 0)
    print("Apagué el láser")


if __name__ == '__main__':
    disparar()