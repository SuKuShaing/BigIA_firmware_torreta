const spawn = require("child_process").spawn; //Spawn permite generar subprocesos con los que se puede interactuar
obj = { Cosa: "ObjCosa", booleano: true, numero: 908 };
const pythonProcess = spawn("python", ["test.py", "otra entrada 1", 1234, 2, JSON.stringify(obj)]); //spawn recibe dos entradas, el proceso a ejecutar y la lista de argumentos del proceso
// const pythonProcess = spawn("python", ["--version"]) //responde dando la versión de python

let pythonResponse = "";

pythonProcess.stdout.on("data", function(data) { //cada vez que el proceso graba datos en sys.stdout se pasan a data y es recibido en data
    pythonResponse += data.toString();
});

pythonProcess.stdout.on("end", function() { //con end detectamos el termino de envío de datos
    // console.log(pythonResponse);
    
    objs = JSON.parse(pythonResponse) //para convertir un Json en objeto js
    console.log(objs); //para convertir un Json en objeto js
    console.log(objs["numero"]*3);

    // console.log(pythonResponse.split("'")[5]*9); //.split("'") corta el string y lo convierte en array, y uno puede seleccionar un item del array y si es número multiplicarlo
    // console.log(pythonResponse*9); //si envía un número lo recibe como tal
});

pythonProcess.stderr.on("data",(data) => { //sí hay un error en el procesamiento será mostrado aquí
    console.error("stderr: " + data);
 });

pythonProcess.on('close',(code) => { //Procesos hijos con codigo
    console.log("child process exited with code: " + code);
});

pythonProcess.stdin.write("Sebitax"); //enviamos datos al subproceso
pythonProcess.stdin.end(); //finalizamos el envío de datos