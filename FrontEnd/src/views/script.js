//Esto se ocupara para los movimientos desde el teclado
var teclas = {
  UP: 38,
  DOWN: 40,
  LEFT: 37,
  RIGHT: 39
}
document.addEventListener("keydown", moverFondoTeclado); //keydown detecta una tecla presionada, keyup cuando se suelta una tecla

//Posición inicial de la camara con respecto al fondo
var posX = 1024;
var posY = 768;

var bbb = document.getElementById('bod'); //trae el elemento a modificar el CSS

//Esto hace que se dibuje y funcione el Joystick
function init() {

  var xCenter = 150;// Damos la posición al Joystick
  var yCenter = 150;
  var stage = new createjs.Stage('joystick');
        
  var psp = new createjs.Shape();
  psp.graphics.beginFill('#333333').drawCircle(xCenter, yCenter, 50);

  psp.alpha = 0.8;

  var vertical = new createjs.Shape();
  var horizontal = new createjs.Shape();
  
  //Lineas para establecer el centro del Joystick
  vertical.graphics.beginFill('#ff4d4d').drawRect(150, 0, 2, 300);
  horizontal.graphics.beginFill('#ff4d4d').drawRect(0, 150, 300, 2);

  stage.addChild(psp);
  stage.addChild(vertical);
  stage.addChild(horizontal);
  createjs.Ticker.framerate = 60;
  createjs.Ticker.addEventListener('tick', stage);
  stage.update();

  var myElement = $('#joystick')[0];

  // crea una instancia simple de la librería Hammer
  // por defecto, solo agrega reconocedores horizontales
  var mc = new Hammer(myElement);

  mc.on("panstart", function(ev) {
    var pos = $('#joystick').position();
    xCenter = psp.x;
    yCenter = psp.y;
    psp.alpha = 0.5;
    
    stage.update();
  });
  
  // Escucha los tactos de los dedo o del mouse
  mc.on("panmove", function(ev) {
    var pos = $('#joystick').position();

    var x = (ev.center.x - pos.left - 150);
    var y = (ev.center.y - pos.top - 150);

    //Esto envía el texto al HTML
    $('#xVal').text('X: ' + Math.floor(x) + ' ');
    $('#yVal').text('Y: ' + (-1 * Math.floor(y)));
    
    var coords = calculateCoords(ev.angle, ev.distance);
    
    psp.x = coords.x;
    psp.y = coords.y;
    
    // console.log("Coords.X: " + Math.floor(psp.x) + ", Coords.Y: " + Math.floor(psp.y));
    //Seba usar las coordenadas para mover la mira 

    moverFondo(psp.x, psp.y);

    psp.alpha = 0.5;
    
    stage.update();
  });
  
  mc.on("panend", function(ev) {
    psp.alpha = 0.25;
    createjs.Tween.get(psp).to({x:xCenter,y:yCenter},750,createjs.Ease.elasticOut);
  });
}

//Esto hace que mueva el fondo con el teclado
function moverFondoTeclado(evento) {
  // console.log(bbb.style.backgroundPosition) => ESTO NO MUESTRA NADA
  
  switch(evento.keyCode){
    case teclas.DOWN:
      posY -= 5;  
      console.log("Pa' abajo weeeyyy");
    break;
    case teclas.UP: 
      posY += 5;  
      console.log("Pa' arriba");
    break;
    case teclas.RIGHT:
      posX -= 5;
      console.log("Pa' derecha");
    break;
    case teclas.LEFT:
      posX += 5;
      console.log("Pa' izquierda");
    break;
    default:
      console.log("Otra tecla");
    break
  }
  
  socket.emit('coordAlServidor', {
    posX,
    posY
  })
  // fondo(posX, posY);
}

//Esto hace que mueva el fondo con las ordenes de Joystick
function moverFondo(coorX, coorY) {
  
  posX -=  Math.floor(coorX/10);
  posY -=  Math.floor(coorY/10);
  
  socket.emit('coordAlServidor', {
    posX,
    posY
  })
  // fondo(posX, posY);
}

//Esto graba la posición en el fondo CSS
function fondo(posX, posY) {
  bbb.style.backgroundPosition = posX + "px " + posY +"px";
}

//Esta funcion calcula las coordenadas del Joystick
function calculateCoords(angle, distance) {
    var coords = {};
    distance = Math.min(distance, 100);  
    var rads = (angle * Math.PI) / 180.0;
  
    coords.x = distance * Math.cos(rads);
    coords.y = distance * Math.sin(rads);
    
    return coords;
}

//Comunicación con el servidor, web socket
const socket = io();

socket.on('coordDelServidor', (data) => {
  fondo(data.posX, data.posY);
  console.log(data);
});

function fuego(){
  socket.emit('pyt')
}


