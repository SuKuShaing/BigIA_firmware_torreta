# Importar librerias
import RPi.GPIO as GPIO
import time
import pygame
from herramientas import (Servo, set_angulo, set_limites, mover_servo, reset)

pygame.init()
ventana = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Torreta")

incremento = 15     # Incremento general de angulos, puede customizarse

# --- SETEAR ENTRADAS (columna 1 : interior arriba)
# reset_posiciones =   # boton para restaurar las posiciones iniciales 
# interruptor =        # palanca para habilitar disparo 

# --- SETEAR SALIDAS (columna 2 : exterior abajo)
# salida_L = 11  # senal para laser
salida_X = 11  # senal para servo de mov horizontal
salida_Y = 12  # senal para servo de mov vertical
# salida_D = 40  # senal para servo disparador


# --- INSTANCIAS DE LOS SERVOS


servo_X = Servo(salida_X)



set_angulo(servo_X, 90)    # angulos iniciales



# Establecer limites de operacion
set_limites(servo_X, 0, 180)    # servo, min, max
#set_limites(servo_Y, 0, 90)     # servo, min, max
#set_limites(servo_D, 30, 160)  # servo, min, max

EN_CURSO = True
while EN_CURSO:

    # Atender eventos
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            EN_CURSO = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for i in range(incremento):    
                    new_angulo = servo_X.angulo - 1
                    mover_servo(servo_X, new_angulo)
                print("Mover a la izquierda")
                
            if event.key == pygame.K_RIGHT:
                new_angulo = servo_X.angulo + incremento
                mover_servo(servo_X, new_angulo)
                print("Mover a la derecha")
    
            if event.key == pygame.K_r:
                set_angulo(servo_X, 90)    # angulos iniciales
                #set_angulo(servo_Y, 0)
                # set_angulo(servo_D, 30)
        
            if event.key == pygame.K_ESCAPE:
                EN_CURSO = False

pygame.quit()