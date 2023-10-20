# Repositorio Numérico 🤖

## Proyecto Torreta
Se lleva a cabo el desarrollo de la torreta automatica de defensa

### Permisos
Para solicitar permisos, avisar a Seba :D

## Crear y ejecutar un entorno virtual
Siempre es importante trabajar dentro de un entorno, puesto que así evitamos que se contaminen las librerías que usamos en cada proyecto, con las librerías de otros proyectos.
Seguir estos pasos en órden, el símbolo "$" indica que lo que sigue se debe pegar en la consola

// se van a crear carpetas del entorno 
// -m : modulo
// venv : Virtual environment
// el último "venv" es el nombre de la carpeta a crear, se puede cambiar, pero lo dejamos así porque todos lo usan así

$ py -m venv venv

// Después de crearlo, hay que activarlo con los siguientes comandos

$ source vent/bin/activate          // para Linux y mac
$ .\venv\Scripts\activate           // Usando W10 con Cmder o equivalentes
$ source ./venv/Scripts/activate    // para w10 usando bash o equivalentes

// para salir del entorno virtual

$ deactivate


## Opcionales
//para crear alias

// para ahorrarse escritura en la activación y solo escribir "avenv"

$ alias avenv=.\venv\Scripts\activate
$ avenv // se activa el modo de Virtual Environment

// para ver todas las dependencias o módulos instalados en el entorno virtual
$ pip freeze 

// Para instalar librerías
$ pip install [nombre de la librería]
$ pip install pandas

// Para guardar las dependencias y que otra persona pueda instalarlas y usarlas igual
pip freeze > requirements.txt 

// Para instalar todas las dependencias de otra persona
pip install -r requirements.txt