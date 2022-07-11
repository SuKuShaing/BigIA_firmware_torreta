const http = require('http');
const fs = require('fs');

const host = '127.0.0.1';
const port = 1311;

const server = http.createServer((req, res) => {
    res.writeHead(200, {'Content-type': 'text/html'});
    fs.readFile('./index.html', (error, data) => {
        if (error) {
            res.writeHead(404);
            res.write('Archivo no encontrado');
        } else {
            res.write(data);
        }
        res.end();
    })
    fs.readFile('./script.js', (error, data) => {
        if (error) {
            res.writeHead(404);
            res.write('Archivo no encontrado');
        } else {
            res.write(data);
        }
        res.end();
    })
    fs.readFile('./style.css', (error, data) => {
        if (error) {
            res.writeHead(404);
            res.write('Archivo no encontrado');
        } else {
            res.write(data);
        }
        res.end();
    })
    // res.write('Hola desde el servidor');
    // res.end();
});

server.listen(port, host, () => {
    console.log('Servidor funcionando en', host, port);
});