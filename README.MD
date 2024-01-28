# Repositorio Numérico 🤖

## Proyecto Torreta
Se lleva a cabo el desarrollo de la torreta automatica de defensa

### Permisos
Para solicitar permisos, avisar a Seba :D

## Crear y ejecutar un entorno virtual
Siempre es importante trabajar dentro de un entorno, puesto que así evitamos que se contaminen las librerías que usamos en cada proyecto, con las librerías de otros proyectos.
Seguir estos pasos en órden, el símbolo "$" indica que lo que sigue se debe pegar en la consola

### PASO 0: INSTALAR
En Linux y en WSL se debe instalar para ejecutar ambientes virtuales, no es necesario en python de Mac y Windows
$ apt install -y python3-venv


### PASO 1: CREAR EL AMBIENTE
para crear el entorno virtual en una carpeta especifica,
posicionare en esa carpeta y luego escribe en consola
$ py -m venv [nombreCarpetaDondeSeDuplicaPython] : se van a crear carpetas con el entorno
$ py -m venv venv : se van a crear carpetas con el entorno

-m : modulo
venv : Virtual environment

después que se crea, hay que activarlo


### PASO 2: ACTIVARLO
después de crear el ambiente, hay que activarlo con los siguientes comandos 

$ source [nombreDeLaCarpeteAmbiente]/bin/activate : para Linux y mac
$ source venv/bin/activate : para Linux y mac
$ .\venv\Scripts\activate : Usando W10 con Cmder
$ source ./venv/Scripts/activate : para w10 usando bash


### PASO 3: LISTO
puedes usar el ambiente


### PASO 4: SALIR
para salir del entorno virtual
$ deactivate



### OPCIONALES: Crear un alias

$ alias avenv=.\venv\Scripts\activate
$avenv : se activa el modo de Virtual Environment

pip freeze : para ver todas las dependencias o módulos instalados en el entorno virtual

pip install pandas

pip freeze > requirements.txt : para guardar las dependencias y que otra persona pueda instalarlas y usarlas igual

pip install -r requirements.txt : para instalar todas las dependencias


## COMANDOS PARA COMPILAR A C EN WINDOWS
debe haber un archivo setup.py para que contenga las instrucciones del archivo a compilar
$ python setup.py build_ext --inplace