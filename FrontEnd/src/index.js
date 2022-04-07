const express = require('express');
const app = express();
const path = require('path'); //path coloca los "\" o "/" según sea windows o linux

// Settings
app.set('port', 1313);
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
app.listen(app.get('port'), () => {
    console.log('server on port', app.get('port'));
});