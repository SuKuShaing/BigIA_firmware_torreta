import time
from time import sleep
import RPi.GPIO as GPIO


class Stepper():
    """Clase que modela los stepper"""

    def __init__(self, nombre, id):
        self.nombre = nombre
        self.angulo = None
        self.id = id
        self.ROT = 1  # default CW (sentido de giro por defecto, en el sentido de las agujas del reloj)
        self.delay = 0.001  # Tiempo de retardo para el motor (puedes ajustarlo según sea necesario) | valor que dejó Felipe 0.0000608 / 32 | debiese ser 0.010 seg 0 10 ms  | lo mínimo que el DVR8825 es de 1,9 ms
        self.en_ejecucion = False

        # Configuración de los pines DIR (dirección) y STEP (paso) según el ID del motor
        if id == 1:
            self.DIR = 20  # Número de pin GPIO para la dirección del motor 1
            self.STEP = 21  # Número de pin GPIO para el paso del motor 1
        elif id == 2:
            self.DIR = 19  # Número de pin GPIO para la dirección del motor 2
            self.STEP = 26  # Número de pin GPIO para el paso del motor 2


    def mover_stepper(self, sentido, pasos): # Tiempo de retardo para el motor (puedes ajustarlo según sea necesario) | valor que dejó Felipe 0.0000608 / 32 | debiese ser 0.010 seg 0 10 ms  | lo mínimo que el DVR8825 es de 1,9 ms
        # Configura el sentido de giro del motor basado en la entrada del usuario ('CW' para sentido de las agujas del reloj y 'CCW' para sentido contrario)
        if sentido == 'CW':
            self.ROT = 1  # Establece el sentido de rotación como CW (sentido de las agujas del reloj)
            GPIO.output(self.DIR, 1)  # Configura el pin de dirección para el sentido de las agujas del reloj
        elif sentido == 'CCW':
            self.ROT = 0  # Establece el sentido de rotación como CCW (sentido contrario a las agujas del reloj)
            GPIO.output(self.DIR, 0)  # Configura el pin de dirección para el sentido contrario a las agujas del reloj

        if self.en_ejecucion:
            print("La función ya está en ejecución")

        self.en_ejecucion = True

        # Genera el número de pasos especificados
        for x in range(pasos):
            GPIO.output(self.STEP, GPIO.HIGH)  # Prende
            sleep(self.delay)  # Espera el tiempo definido
            GPIO.output(self.STEP, GPIO.LOW)  # apaga
            sleep(self.delay) # TODO: podría ser diferente, Espera el tiempo definido que es el mismos que el de prendido

        self.en_ejecucion = False

    def mover_stepper_debug(self, sentido, pasos, delay=0.01): # Tiempo de retardo para el motor (puedes ajustarlo según sea necesario) | valor que dejó Felipe 0.0000608 / 32 | debiese ser 0.010 seg 0 10 ms  | lo mínimo que el DVR8825 es de 1,9 ms
        # medir el tiempo que demora en ejecutarse la función
        start_time = time.time()

        print(f"Estoy en debugging, entre a la función mover_stepper_debug, pasos: {pasos} y delay: {delay}")
        # Configura el sentido de giro del motor basado en la entrada del usuario ('CW' para sentido de las agujas del reloj y 'CCW' para sentido contrario)
        if sentido == 'CW':
            self.ROT = 1  # Establece el sentido de rotación como CW (sentido de las agujas del reloj)
            GPIO.output(self.DIR, 1)  # Configura el pin de dirección para el sentido de las agujas del reloj
        elif sentido == 'CCW':
            self.ROT = 0  # Establece el sentido de rotación como CCW (sentido contrario a las agujas del reloj)
            GPIO.output(self.DIR, 0)  # Configura el pin de dirección para el sentido contrario a las agujas del reloj

        for paso in range(pasos):
            GPIO.output(self.STEP, GPIO.HIGH)  # Prende 
            sleep(delay)  # Espera el tiempo definido
            GPIO.output(self.STEP, GPIO.LOW)  # apaga
            sleep(delay) # TODO: podría ser diferente, Espera el tiempo definido que es el mismos que el de prendido
            # cada 100 pasos el if se cumple
            if paso % 100 == 0:
                print(f"Estoy en tools_web, en el paso: {paso} y delay: {delay}")

        # Termina de medir el tiempo que demora en ejecutarse la función
        elapsed_time = time.time() - start_time
        print(f"Tiempo de ejecución de la función mover_stepper_debug: {elapsed_time} segundos")

    def mover_stepper_suave(self, sentido, pasos):
            initial_delay = 0.0001  # Retraso inicial más grande para arranque suave
            final_delay = 0.0000608  # Retraso final más pequeño para velocidad máxima | debería estar dividido entre 32

            if sentido == 'CW':
                self.ROT = 1
                GPIO.output(self.DIR, 1)
            elif sentido == 'CCW':
                self.ROT = 0
                GPIO.output(self.DIR, 0)

            for paso in range(pasos):
                # Aplicar un perfil de aceleración
                acceleration_factor = paso / pasos  # Ajuste de aceleración gradual, "pasos" en cuantos pasos va a hacer la aceleración y llegar al máximo de velocidad
                current_delay = initial_delay + (final_delay - initial_delay) * acceleration_factor # para el acelerado 
                # current_delay = final_delay + (initial_delay - final_delay) * acceleration_factor # para el frenado 

                GPIO.output(self.STEP, GPIO.HIGH)
                sleep(current_delay)
                GPIO.output(self.STEP, GPIO.LOW)
                sleep(current_delay)


"""
Video maestro, contiene como hacer bien el software, microsteping, uso de pwm para no bloquear el hilo de la CPU
https://youtu.be/LUbhPKBL_IU?si=IOu-vKIIJUFf_AhC
su blog 
https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/

delay máximo (tiempo mínimo de paso para el motor nema) 0,0005 seg
delay optimo (tiempo mínimo de paso para el motor nema) 0,001 seg
delay mínimo (tiempo mínimo de paso para el motor nema) 0,05 seg (se puede menos, pero este está bien)
"""