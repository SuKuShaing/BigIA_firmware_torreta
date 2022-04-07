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