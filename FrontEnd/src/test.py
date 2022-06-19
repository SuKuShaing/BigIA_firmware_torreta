# from ast import operator
import sys  #libreria que nos permite recibir info
import json #para formatear los datos salientes
# import ast #librería árbol de sintaxis abstracta

nombre = sys.stdin.readline() #lee lo enviado por js y lo guardamos en una variable

#Aquí se procesa la información recibida
# print("Output from Python")
# print("que tal madafaka", nombre)
# print("str(sys.argv): ", str(sys.argv))
# print("str(sys.argv[1]): ", str(sys.argv[1]))
# print("str(sys.argv[2]): ", str(sys.argv[2]))
# print("str(sys.argv[3]): ", str(sys.argv[3]))
# print("str(sys.argv[4]): ", str(sys.argv[4]))
# print(str(sys.argv))


############# Trabajar con JSON ################
obto_py = json.loads(str(sys.argv[4])) #con json.loads convertimos un Json en un objeto python 
obto_py['numero'] = obto_py['numero'] * 3
obto_py['coorX'] = obto_py['numero'] * 3
obto_py['booleano'] = False
# print(obto_py) #json.dumps convertimos un objeto python a Json
print(json.dumps(obto_py)) #json.dumps convertimos un objeto python a Json


############# ARRAYS ################
# a = int(str(sys.argv[2])) #sí se recibe un número, se recibe como texto, con "int("n")" se convierte a número 
# b = int(str(sys.argv[3]))
# c = a / b 
# print("resultado de la division: ", c)
# print(c)

sys.stdout.flush() #Fuerza la salida de datos y los envía a quien nos envió la info en primer lugar
