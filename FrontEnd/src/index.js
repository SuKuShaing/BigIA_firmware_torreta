/* 
Seba: para iniciar esto tienes que ir con la consolo hasta donde está el archivo
index.js y a ese archivo debes darle en la consola "node index.js" para que se inicie el servidor
y ahora pueda andar, ahora al ejecuar index.html, se podrá mover el fondo, puesto que
el joystick envia el comando al servidor y éste lo regresa al html como un fondo corrido
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
});

/*
Información para el desarrollo, videos tutoriales

HTML5, Nodejs, Express, WebSockets y Mongodb
https://www.youtube.com/watch?v=s_Stz1KlSdo&list=RDCMUCX9NJ471o7Wie1DQe94RVIg&index=2

información Socket.io
https://youtu.be/0wqteZNqruc
*/

const spawn = require("child_process").spawn

const pythonProcess = spawn("python", ["test.py"])

let pythonResponse = ""

pythonProcess.stdout.on("data", function(data) {
    pythonResponse += data.toString()
})

pythonProcess.stdout.on("end", function() {
    console.log(pythonResponse)
})

pythonProcess.stdin.write("Sebendi")

pythonProcess.stdin.end()