# Importar librerias
import RPi.GPIO as GPIO
import time
import pygame
from herramientas import (Servo, set_angulo, set_limites, mover_servo, reset)

clock = pygame.time.Clock()
pygame.init()
ventana = pygame.display.set_mode((300, 200))


# Setiar GPIO modo numeracion
GPIO.setmode(GPIO.BOARD)
freq = 53.5        # 53.5 Hz de pulso
incremento = 5     # Incremento general de angulos, puede customizarse

# --- SETEAR ENTRADAS (columna 1 : interior arriba)
# reset_posiciones = 7  # boton para restaurar las posiciones iniciales 
# interruptor = 11      # palanca para habilitar disparo 

# --- SETEAR SALIDAS (columna 2 : exterior abajo)
# salida_L = 11  # senal para laser
salida_X = 11  # senal para servo de mov horizontal
salida_Y = 12  # senal para servo de mov vertical
# salida_D = 40  # senal para servo disparador

GPIO.setup(salida_X, GPIO.OUT)
# GPIO.setup(salida_Y, GPIO.OUT)
# GPIO.setup(salida_D, GPIO.OUT)
# GPIO.setup(salida_L, GPIO.OUT)

# --- INSTANCIAS DE LOS SERVOS

#servo_X = GPIO.PWM(salida_X, freq)
#servo_Y = GPIO.PWM(salida_Y, freq)
#servo_D = GPIO.PWM(salida_D, freq)
servo_X = Servo(salida_X, freq)
#servo_Y = Servo(salida_Y, freq)


set_angulo(servo_X, 90)    # angulos iniciales
#set_angulo(servo_Y, 0)
# set_angulo(servo_D, 30)


# Establecer limites de operacion
set_limites(servo_X, 0, 180)    # servo, min, max
#set_limites(servo_Y, 0, 90)     # servo, min, max
#set_limites(servo_D, 30, 160)  # servo, min, max

EN_CURSO = True
while EN_CURSO:
    # Recepcion de input por Joystick
    key = pygame.key.get_pressed()
    
    if key[pygame.K_LEFT]:
        new_angulo = servo_X.angulo - incremento
        mover_servo(servo_X, new_angulo)
        print("Mover a la izquierda")

    if key[pygame.K_RIGHT]:
        new_angulo = servo_X.angulo + incremento
        mover_servo(servo_X, new_angulo)
        print("Mover a la derecha")
        
    #if key[pygame.K_UP]:  # inclinarse hacia abajo
    #    new_angulo = servo_Y.angulo + incremento
    #    mover_servo(servo_Y, new_angulo)
        
    #if key[pygame.K_DOWN]:  # inclinarse hacia arriba
    #    new_angulo = servo_Y.angulo - incremento
    #    mover_servo(servo_Y, new_angulo)
        
    if key[pygame.K_r]:  # reseteo de angulos
        set_angulo(servo_X, 90)    # angulos iniciales
        #set_angulo(servo_Y, 0)
        # set_angulo(servo_D, 30)
        
    if key[pygame.K_ESCAPE]: # para terminar programa
        EN_CURSO = False