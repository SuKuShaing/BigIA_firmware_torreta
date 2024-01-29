import time
# from time import sleep
from libc.time cimport usleep
import RPi.GPIO as GPIO
import queue
import threading
import cython


cdef class Stepper():
    """Clase que modela los stepper"""

    cdef str nombre
    cdef object angulo
    cdef int id, ROT, DIR, STEP
    cdef float delay

    def __init__(self, str nombre, int id):
        self.nombre = nombre
        self.angulo = None
        self.id = id
        self.ROT = 1  # default CW (sentido de giro por defecto, en el sentido de las agujas del reloj)
        self.delay = 0.001 * 1000000 # Tiempo de retardo para el motor (puedes ajustarlo según sea necesario) | valor que dejó Felipe 0.0000608 / 32 | debiese ser 0.010 seg 0 10 ms  | lo mínimo que el DVR8825 es de 1,9 ms

        # Configuración de los pines DIR (dirección) y STEP (paso) según el ID del motor
        if id == 1:
            self.DIR = 20  # Número de pin GPIO para la dirección del motor 1
            self.STEP = 21  # Número de pin GPIO para el paso del motor 1
        elif id == 2:
            self.DIR = 19  # Número de pin GPIO para la dirección del motor 2
            self.STEP = 26  # Número de pin GPIO para el paso del motor 2


    cpdef mover_stepper(self, str sentido, int pasos): # Tiempo de retardo para el motor (puedes ajustarlo según sea necesario) | valor que dejó Felipe 0.0000608 / 32 | debiese ser 0.010 seg 0 10 ms  | lo mínimo que el DVR8825 es de 1,9 ms
        cdef int x
    
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
            usleep(self.delay)  # Espera el tiempo definido
            GPIO.output(self.STEP, GPIO.LOW)  # apaga
            usleep(self.delay) # TODO: podría ser diferente, Espera el tiempo definido que es el mismos que el de prendido


    cpdef mover_stepper_debug(self, str sentido, int pasos, double delay=0.01): # Tiempo de retardo para el motor (puedes ajustarlo según sea necesario) | valor que dejó Felipe 0.0000608 / 32 | debiese ser 0.010 seg 0 10 ms  | lo mínimo que el DVR8825 es de 1,9 ms
        cdef double start_time, elapsed_time
        cdef int paso

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
            usleep(delay)  # Espera el tiempo definido
            GPIO.output(self.STEP, GPIO.LOW)  # apaga
            usleep(delay) # TODO: podría ser diferente, Espera el tiempo definido que es el mismos que el de prendido
            # cada 100 pasos el if se cumple
            if paso % 100 == 0:
                print(f"Estoy en tools_web, en el paso: {paso} y delay: {delay}")

        # Termina de medir el tiempo que demora en ejecutarse la función
        elapsed_time = time.time() - start_time
        print(f"Tiempo de ejecución de la función mover_stepper_debug: {elapsed_time} segundos")

    cpdef mover_stepper_suave(self, str sentido, int pasos):
            cdef double initial_delay = 0.0001 * 1000000
            cdef double final_delay = 0.0000608 * 1000000
            cdef double acceleration_factor, current_delay
            cdef int paso

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
                usleep(current_delay)
                GPIO.output(self.STEP, GPIO.LOW)
                usleep(current_delay)

    cpdef mover_infinito(self, object cola):
        cdef int pasos_que_llevo = 0
        cdef int pasos_que_llevo_maximos = int((45/360)*200*1)
        cdef int pasos_a_ejecutar = 0
        cdef list datos = []
        cdef double delay_inicial = 0.01 * 1000000
        cdef double delay_final = 0.0001 * 1000000
        cdef double start_time, elapsed_time, acceleration_factor, current_delay


        print(f"Inicie el thread del motor {self.id}")
        while True:
            start_time = time.time()

            if not cola.empty():
                for i in range(cola.qsize()):
                    datos.append(cola.get())

                mismo_signo = True
                for x in datos:
                    if x < 0:
                        mismo_signo = False
                        break
                if not mismo_signo:
                    for x in datos:
                        if x >= 0:
                            mismo_signo = False
                            break


                if mismo_signo:
                    # Dirección del giro en base al primer elemento de la lista
                    if datos[0] >= 0:
                        # 'CW'
                        self.ROT = 1
                        GPIO.output(self.DIR, 1)
                        print("CW")
                    elif datos[0] < 0:
                        self.ROT = 0
                        GPIO.output(self.DIR, 0)
                        print("CCW")

                    pasos_a_ejecutar = 0
                    for dato in datos:
                        pasos_a_ejecutar += abs(dato)
                    datos.clear()
                else:
                    print("Hay un signo opuesto en la lista de datos")
                    pasos_a_ejecutar = pasos_que_llevo
                    datos.clear()

            if pasos_a_ejecutar > 0:
                if pasos_a_ejecutar > pasos_que_llevo:
                    if pasos_que_llevo < pasos_que_llevo_maximos:
                        # modo aceleración
                        acceleration_factor = pasos_que_llevo / pasos_que_llevo_maximos  # Ajuste de aceleración gradual, "pasos" en cuantos pasos va a hacer la aceleración y llegar al máximo de velocidad
                        current_delay = delay_inicial + (delay_final - delay_inicial) * acceleration_factor # para el acelerado 
                        # current_delay = delay_final + (delay_inicial - delay_final) * acceleration_factor # para el acelerado 

                        GPIO.output(self.STEP, GPIO.HIGH)
                        usleep(current_delay)
                        GPIO.output(self.STEP, GPIO.LOW)
                        usleep(current_delay)

                        pasos_que_llevo += 1
                    else:
                        # modo velocidad constante
                        GPIO.output(self.STEP, GPIO.HIGH)
                        usleep(delay_final)
                        GPIO.output(self.STEP, GPIO.LOW)
                        usleep(delay_final)
                else:
                    # modo frenado
                    acceleration_factor = pasos_que_llevo / pasos_que_llevo_maximos  # Ajuste de aceleración gradual, "pasos" en cuantos pasos va a hacer la aceleración y llegar al máximo de velocidad
                    # current_delay = delay_final + (delay_inicial - delay_final) * acceleration_factor
                    current_delay = (delay_inicial - delay_final) * (1 - acceleration_factor) + delay_final # para el frenado
                    
                    GPIO.output(self.STEP, GPIO.HIGH)
                    usleep(current_delay)
                    GPIO.output(self.STEP, GPIO.LOW)
                    usleep(current_delay)

                    pasos_que_llevo -= 1
                    pasos_que_llevo = max(0, pasos_que_llevo)

                pasos_a_ejecutar -= 1
                pasos_a_ejecutar = max(0, pasos_a_ejecutar)

                elapsed_time = time.time() - start_time
                print(f"Tiempo de ejecución de la función mover_stepper_debug: {elapsed_time} segundos")


#######################################################
############## Declaración de Variables ###############
#######################################################

# Incremento general de pasos, puede personalizarse
# Declaración de tipos estáticos
cdef int incremento = 10, aumento_incremento = 5

cdef int DIR1 = 20, STEP1 = 21, CW1 = 1, CCW1 = 0
cdef int DIR2 = 19, STEP2 = 26, CW2 = 1, CCW2 = 0

cdef int[3] MODE1 = [14, 15, 18]  # Mode 0, Mode 1, Mode 2
cdef int[3] MODE2 = [17, 27, 22]  # Mode 0, Mode 1, Mode 2

# Asignación de pines
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR1, GPIO.OUT) # 20 en high
GPIO.setup(STEP1, GPIO.OUT) # 21 en high
GPIO.output(DIR1, CW1)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(STEP2, GPIO.OUT)
GPIO.output(DIR2, CW2)
GPIO.setup(MODE1, GPIO.OUT)
GPIO.setup(MODE2, GPIO.OUT)
GPIO.output(MODE1, (0, 0, 0)) # De aquí se regula el microstepping
GPIO.output(MODE2, (0, 0, 0)) # Microstepping Resolution GPIO


#######################################################
################# Iniciar los motores #################
#######################################################

# aquí va la instancia de cola para cada motor
cola_m1 = queue.Queue()
cola_m2 = queue.Queue()

# INSTANCIAS DE LOS STEPPER
m1 = Stepper("M1", 1)
m2 = Stepper("M2", 2)

# se instancia el thread para cada motor
thread_m1 = threading.Thread(target=m1.mover_infinito, args=(cola_m1,))
thread_m2 = threading.Thread(target=m2.mover_infinito, args=(cola_m2,))

thread_m1.start()
thread_m2.start()

#######################################################
###################### Funciones ######################
#######################################################

cpdef mov_izquierda_prueba(int pasos, float tiempoHigh):
    # print(f'Estoy en torr_v2_web, pasos: {pasos} y tiempoHigh: {tiempoHigh}')
    m1.mover_stepper_debug('CCW', pasos, tiempoHigh)


cpdef mov_izquierda():
    # m1.mover_stepper('CCW', incremento)
    global incremento
    cola_m1.put(-incremento)
    print(f"Puse en cola {incremento} pasos a la izquierda")


cpdef mov_derecha():
    # m1.mover_stepper('CW', incremento)
    global incremento
    cola_m1.put(incremento)
    print(f"Puse en cola {incremento} pasos a la derecha")


cpdef mov_arriba():
    # m2.mover_stepper('CW', incremento)
    global incremento
    cola_m2.put(incremento)
    print(f"Puse en cola {incremento} pasos arriba")


cpdef mov_abajo():
    # m2.mover_stepper('CCW', incremento)
    global incremento
    cola_m2.put(-incremento)
    print(f"Puse en cola {incremento} pasos abajo")


cpdef aum_vel_mov():
    global incremento
    global aumento_incremento
    incremento += aumento_incremento
    print(f'Pasos por click o incremento es de: {incremento}')
    # print('Recordar el valor máximo de pasos por click, el limite de velocidad del motor')


cpdef dis_vel_mov():
    global incremento
    global aumento_incremento
    if incremento > aumento_incremento:
        incremento -= aumento_incremento
        print(f'Pasos por click o incremento es de: {incremento}')
    else:
        print('Pasos por click o incremento llegaría a cero, Explorar que pasa en esta situación')