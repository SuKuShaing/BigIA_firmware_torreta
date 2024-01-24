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

        # Genera el número de pasos especificados
        for x in range(pasos):
            GPIO.output(self.STEP, GPIO.HIGH)  # Prende
            sleep(self.delay)  # Espera el tiempo definido
            GPIO.output(self.STEP, GPIO.LOW)  # apaga
            sleep(self.delay) # TODO: podría ser diferente, Espera el tiempo definido que es el mismos que el de prendido


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

    def mover_infinito():
        while True:
            pass
            
            # Se obtienen todos los datos de la cola con un for y se pasan a una lista
                # se analizan en busca si hay un cambio de dirección, sino hay, se suman todos los pasos y se guardan en pasos a ejecutar
                # si hay una cambio de dirección, se ejecuta el cambio de dirección pasando "solo 100 pasos" para que frene o una opción de freno 
            
            # pasos_a_ejecutar
            # pasos_que_llevo, (velocidad_que_llevo), cuenta cuantos pasos que lleva para elegir el modo de velocidad a ejecutar
                # Evaluó los pasos que llevo y en que estoy, entre 0 a 100 mayor o mayor a 100 (teniendo en cuenta que 100 es solo una referencia, dado es el 45° por su equivalente en pasos, ese es el espacio que me voy a tomar para acelerar y frenar, puede ser menos)
                # ahora hay que hacer una división pasos_a_ejecutar / 2, si es mayor a (100/2) ejecutar el modo aceleración y los pasos_a_ejecutar son mayores a los pasos_que_llevo acelerar
                    # modo aceleración, tomo la velocidad (pasos_que_llevo) y voy aumentando la velocidad hasta llegar a la velocidad máxima constante
                # si es menor a (100/2) ejecutar el modo frenado con los pasos a ejecutar o los pasos_que_llevo son iguales o menor a los pasos_a_ejecutar, frenar
                    # modo frenado, le paso los 100 y voy disminuyendo la velocidad hasta llegar a cero, ambos deben llegar a cero

                # disminuyo en uno los pasos_a_ejecutar, después de cada pasada


"""
Video maestro, contiene como hacer bien el software, microsteping, uso de pwm para no bloquear el hilo de la CPU
https://youtu.be/LUbhPKBL_IU?si=IOu-vKIIJUFf_AhC
su blog 
https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/

Para Pasos enteros:
    delay máximo (tiempo mínimo de paso para el motor nema) 0,0005 seg
    delay optimo (tiempo mínimo de paso para el motor nema) 0,001 seg
    delay mínimo (tiempo mínimo de paso para el motor nema) 0,05 seg (se puede menos, pero este está bien)

Para microstepping de 1/32:
    delay máximo (Colocando un número más chico, no hay aumento en la velocidad de giro)    0,00001 seg
    delay optimo (tiempo optimo)                                                            0,0001 seg
    delay mínimo (Un número más grande que eso gira muy lento)                              0,001 seg
"""


"""
def while true:
    obtener todos los elementos de la cola en una dirección, se suman

    se pasan a una variable que mantiene la cantidad_de_pasos

    if contar_pasos < cantidad_de_pasos:
        if contar_pasos < 100:
            mover_stepper con curva de aceleración
        if contar_pasos >= 100:
            mover_stepper a velocidad maxima constante
        if cantidad_de_pasos - contar_pasos > 100:
            frenar con curva de desaceleración
        contar_pasos += 1


En la variable que mantiene la cantidad de pasos colocar un condicional 
por si es que el usuario cambia de dirección cosa de que frene y cambia de dirección

que si va en una dirección u en otra, con el joistick 
"""