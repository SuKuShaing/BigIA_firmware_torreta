# Importar librerias
import time
from time import sleep
import numpy as np
import pygame
from picamera import PiCamera
import RPi.GPIO as GPIO
import threading as th
from threading import Event
from tools import Stepper


camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview(fullscreen=False, window = (100, 20, 640, 480))
camera.rotation = 180

pygame.init()
ventana = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Torreta")
pygame.key.set_repeat(1, 10)

incremento = 100     # Incremento general de pasos, puede customizarse

# Pines
DIR1 = 20    
STEP1 = 21   
CW1 = 1      
CCW1 = 0     
DIR2 = 19   
STEP2 = 26   
CW2 = 1      
CCW2 = 0     

# Disparador

SHOT = 25
MODE1 = (14, 15, 18)  
MODE2 = (17, 27, 22)  

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(STEP1, GPIO.OUT)
GPIO.output(DIR1, CW1)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(STEP2, GPIO.OUT)
GPIO.output(DIR2, CW2)
GPIO.setup(SHOT, GPIO.OUT)
GPIO.setup(MODE1, GPIO.OUT)
GPIO.setup(MODE2, GPIO.OUT)
GPIO.output(MODE1, (0, 0, 0))
GPIO.output(MODE2, (0, 0, 0))


# --- INSTANCIAS DE LOS STEPPER --- 

m1 = Stepper("M1", 1)  
m2 = Stepper("M2", 2)


EN_CURSO = True
while EN_CURSO:

    # Atender eventos
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            EN_CURSO = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:    
                m1.mover_stepper('CCW', incremento)
                print("Mover a la izquierda")

            if event.key == pygame.K_RIGHT:
                m1.mover_stepper('CW', incremento)
                print("Mover a la derecha")

            if event.key == pygame.K_UP:    
                m2.mover_stepper('CW', incremento)
                print("Mover arriba")

            if event.key == pygame.K_DOWN:
                m2.mover_stepper('CCW', incremento)
                print("Mover abajo")

            if event.key == pygame.K_r:  # Reset usando tecla r
                print("Reseteando posiciones")
            
            if event.key == pygame.K_f:
                incremento = 300
                print("Modo rapido")

            if event.key == pygame.K_s:
                incremento = 200
                print("Modo detalle")
                
            if event.key == pygame.K_d:
                GPIO.output(SHOT, 1)
                sleep(0.1)
                GPIO.output(SHOT, 0)
                print("Disparo")

            if event.key == pygame.K_ESCAPE:
                EN_CURSO = False
                camera.stop_preview()
                camera.close()
                

print("Cerrando programa ...")
pygame.quit()