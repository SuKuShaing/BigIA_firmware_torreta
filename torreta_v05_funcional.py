# Importar librerias
import time
import pygame
from picamera import PiCamera
from herramientas_v2 import Servo, laser, read_sensor_mov

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
#camera.rotation = 180

pygame.init()
ventana = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Torreta")
pygame.key.set_repeat(1, 10)


incremento = 2     # Incremento general de angulos, puede customizarse

# --- SETEAR ENTRADAS (columna 1 : interior arriba)
# reset_posiciones =   # boton para restaurar las posiciones iniciales 
# interruptor =        # palanca para habilitar disparo 

# --- SETEAR SALIDAS (columna 2 : exterior abajo)
# salida_L = 7  # senal para laser
salida_X = 11  # senal para servo de mov horizontal
salida_Y = 12  # senal para servo de mov vertical
salida_D = 13  # senal para servo disparador


# --- INSTANCIAS DE LOS SERVOS --- params: pin, id

servo_X = Servo(salida_X, 'X')  
servo_Y = Servo(salida_Y, 'Y')
servo_D = Servo(salida_D, 'D')

# Establecer limites de operacion : min, max
servo_X.set_limites(0, 180)      
servo_Y.set_limites(0, 90)
servo_D.set_limites(0, 140)

# Establecer las referencias : angulo_inicial
servo_X.set_referencias(90)
servo_Y.set_referencias(0)
servo_D.set_referencias(50)

# Mover servos a posiciones iniciales
servo_X.inicio()
time.sleep(0.2)
servo_Y.inicio()
time.sleep(0.2)
servo_D.inicio()
time.sleep(0.2)
print("Posiciones Iniciales")


EN_CURSO = True
while EN_CURSO:
    # Lectura del sensor de movimiento
    read_sensor_mov()    

    # Atender eventos
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            EN_CURSO = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:    
                new_angulo = servo_X.angulo - incremento
                servo_X.mover_servo(new_angulo)
                print("Mover a la izquierda")
                
            if event.key == pygame.K_RIGHT:
                new_angulo = servo_X.angulo + incremento
                servo_X.mover_servo(new_angulo)
                print("Mover a la derecha")
                
            if event.key == pygame.K_UP:    
                new_angulo = servo_Y.angulo - incremento
                servo_Y.mover_servo(new_angulo)
                print("Mover abajo")
                
            if event.key == pygame.K_DOWN:
                new_angulo = servo_Y.angulo + incremento
                servo_Y.mover_servo(new_angulo)
                print("Mover arriba")
                
            if event.key == pygame.K_RETURN:  # Disparo usando enter
                servo_D.mover_servo(servo_D.max)
                time.sleep(0.6)
                servo_D.mover_servo(servo_D.angulo_inicial)
                time.sleep(0.2)
                print("Disparo")
    
            if event.key == pygame.K_c:  
                new_angulo = servo_D.angulo + incremento
                servo_D.mover_servo(new_angulo)
                print("angulo : {}".format(servo_D.angulo))
                
            if event.key == pygame.K_d:  
                new_angulo = servo_D.angulo - incremento
                servo_D.mover_servo(new_angulo)
                print("angulo : {}".format(servo_D.angulo))
                
            if event.key == pygame.K_r:  # Reset usando tecla r
                servo_X.inicio()
                servo_Y.inicio()
                servo_D.inicio()
                laser(0)
                print("Reseteando posiciones")
            
            if event.key == pygame.K_l:
                laser(1)
                print("Laser activado")
                
            if event.key == pygame.K_o:
                laser(0)
                print("Laser desactivado")
                
            if event.key == pygame.K_f:
                incremento = 8
                print("Modo rapido")
                
            if event.key == pygame.K_s:
                incremento = 2
                print("Modo detalle")
            
            if event.key == pygame.K_ESCAPE:
                EN_CURSO = False
                camera.stop_preview()
                camera.close()

laser(0)
pygame.quit()