# Importar librerias
import RPi.GPIO as GPIO
import time

# Setiar GPIO modo numeracion
GPIO.setmode(GPIO.BOARD)

# Setiar pin 11 como salida
salida = 11
GPIO.setup(salida, GPIO.OUT)

# Crear una instancia de servo
freq = 50  # 50 Hz de pulso
servo_D = GPIO.PWM(salida, freq)

# Comenzar PWM, desde el valor de 0 (pulso apagado)
freq_inicial = 0
servo_D.start(freq_inicial)
pausa = 2  # 2 segundos de espera
print("Espera por 2 segundos")
time.sleep(pausa)

# Comienza a moverse el servo disparador
print("Rotando 180 grados en 10 pasos")

# Definimos la variable duty en 0° -> 2%
duty = 2

# Loop para valores duty desde 2 hasta 12 (0 a 180 grados)
while duty <= 12:
    servo_D.ChangeDutyCycle(duty)
    time.sleep(1)
    duty = duty + 1

# Esperar 2 segundos
time.sleep(pausa)

# Devolverse a 90 grados
print("Devolverse a 90 grados por 2 segundos")
servo_D.ChangeDutyCycle(7)
time.sleep(pausa)

# Devolverse a 0 grados
print("Volver a 0 grados")
servo_D.ChangeDutyCycle(pausa)

time.sleep(0.5)
servo_D.ChangeDutyCycle(0)

# Limpiar todo a la salida
servo_D.stop()
GPIO.cleanup()
print("Chao")