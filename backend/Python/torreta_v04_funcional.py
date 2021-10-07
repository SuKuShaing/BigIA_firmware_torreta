# Importar librerias
import RPi.GPIO as GPIO
import time
import pygame
from herramientas import (Servo, set_angulo, set_limites, mover_servo, reset)

pygame.init()
ventana = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Torreta")
pygame.key.set_repeat(1, 10)

incremento = 5     # Incremento general de angulos, puede customizarse

# --- SETEAR ENTRADAS (columna 1 : interior arriba)
# reset_posiciones =   # boton para restaurar las posiciones iniciales 
# interruptor =        # palanca para habilitar disparo 

# --- SETEAR SALIDAS (columna 2 : exterior abajo)
# salida_L = 11  # senal para laser
salida_X = 11  # senal para servo de mov horizontal
salida_Y = 12  # senal para servo de mov vertical
salida_D = 13  # senal para servo disparador


# --- INSTANCIAS DE LOS SERVOS

servo_X = Servo(salida_X)
servo_Y = Servo(salida_Y)
servo_D = Servo(salida_D)

# Establecer limites de operacion
set_limites(servo_X, 0, 180)    # servo, min, max
set_limites(servo_Y, 0, 90)     # servo, min, max
set_limites(servo_D, 0, 140)  # servo, min, max

# Adoptar posiciones iniciales
mover_servo(servo_X, 90)
mover_servo(servo_Y, 0)
mover_servo(servo_D, 0)
print("Posiciones Iniciales")


EN_CURSO = True
while EN_CURSO:

    # Atender eventos
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            EN_CURSO = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:    
                new_angulo = servo_X.angulo - incremento
                mover_servo(servo_X, new_angulo)
                print("Mover a la izquierda")
                
            if event.key == pygame.K_RIGHT:
                new_angulo = servo_X.angulo + incremento
                mover_servo(servo_X, new_angulo)
                print("Mover a la derecha")
                
            if event.key == pygame.K_UP:    
                new_angulo = servo_Y.angulo - incremento
                mover_servo(servo_Y, new_angulo)
                print("Mover abajo")
                
            if event.key == pygame.K_DOWN:
                new_angulo = servo_Y.angulo + incremento
                mover_servo(servo_Y, new_angulo)
                print("Mover arriba")
                
            if event.key == pygame.K_RETURN:
                mover_servo(servo_D, 140)
                time.sleep(0.6)
                mover_servo(servo_D, 50)
                time.sleep(0.2)
                print("Disparo")
    
            if event.key == pygame.K_d:
                new_angulo = servo_D.angulo + incremento
                mover_servo(servo_D, new_angulo)
                print("angulo : {}".format(servo_D.angulo))
                #mover_servo(servo_D, 140)
                #time.sleep(0.6)
                #mover_servo(servo_D, 50)
                #time.sleep(0.2)
                #print("Disparo")
                
            if event.key == pygame.K_r:
                mover_servo(servo_X, 90)
                mover_servo(servo_Y, 0)
                mover_servo(servo_D, 50)
                print("Reseteando posiciones")
        
            if event.key == pygame.K_ESCAPE:
                EN_CURSO = False

pygame.quit()