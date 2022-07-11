/* 
Seba: para iniciar esto tienes que ir con la consola hasta donde está el archivo
index.js y a ese archivo debes darle en la consola "node index.js" para que se inicie el servidor
y ahora pueda andar, ahora al ejecutar index.html, se podrá mover el fondo, puesto que
el joystick envía el comando al servidor y éste lo regresa al html como un fondo corrido
*/

const express = require('express');
const path = require('path'); //path coloca los "\" o "/" según sea windows o linux
const app = express();


// Settings
app.set('port', process.env.PORT || 1313); //Usa el puesto que le da el servidor o el que yo asigne
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

// middlewares (acciones que uno puede hacer, como autentificaciones)

// routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/views/index.html'));
});

// static files
app.use(express.static(path.join(__dirname, 'views'))); //con esté comando envío el resto de archivos que llamará index

// listening the server
const server = app.listen(app.get('port'), () => {
    console.log('server on port', app.get('port'));
});

//Web Socket
const socketIO = require('socket.io');
const io = socketIO(server);

io.on('connection', (socket) => {
    console.log('new connection', socket.id);

    socket.on('coordAlServidor', (data) => {
        io.sockets.emit('coordDelServidor', data);
    });

    socket.on('pyt', () => {
            aa = Math.trunc(Math.random()*1000);
            fire(aa);
    });
});

/*
Información para el desarrollo, videos tutoriales

HTML5, Nodejs, Express, WebSockets y Mongodb
https://www.youtube.com/watch?v=s_Stz1KlSdo&list=RDCMUCX9NJ471o7Wie1DQe94RVIg&index=2

información Socket.io
https://youtu.be/0wqteZNqruc
*/

///////////////// Ejecución del script de python /////////////////////////////

const spawn = require("child_process").spawn;

function fire (x1) {
    // obj = { Cosa: "ObjCosa", booleano: true, numero: x1, Robin: 32, Seba: "OpenCree" };
    obj = { Hidrogeno: 0.1, Metano: 2, Acetileno: 0.33, Etileno: 4, Etano: 5.5 };
    const pythonProcess = spawn("python", ["test.py", "otra entrada 1", 1234, x1, JSON.stringify(obj)]);
    
    let pythonResponse = "";
    pythonProcess.stdout.on("data", function(data) {
        pythonResponse += data.toString();
    });

    pythonProcess.stdout.on("end", function() {
        // console.log(pythonResponse);
        objs = JSON.parse(pythonResponse) //para convertir un Json en objeto js
        console.log(objs); //para convertir un Json en objeto js
        // console.log(objs["numero"]*3);

    });
    
    pythonProcess.stderr.on("data",(data) => {
        console.error("stderr: " + data);
    });
    
    pythonProcess.on('close',(code) => {
        console.log("child process exited with code: " + code);
    });
    
    pythonProcess.stdin.write("Sebitax"); //enviamos datos al subproceso
    pythonProcess.stdin.end(); //finalizamos el envío de datos
}