var teclas = {
  UP: 38,
  DOWN: 40,
  LEFT: 37,
  RIGHT: 39
}

document.addEventListener("keydown", moverFondoTeclado); //keydown detecta una tecla presionada, keyup cuando se suelta una tecla

var posX = 1024;
var posY = 768;

var bbb = document.getElementById('bod'); //trae el elemento a modificar el CSS

function moverFondoTeclado(evento) {
  // console.log(bbb.style.backgroundPosition) => ESTO NO MUESTRA NADA
  
  //Esto hace que mueva con el teclado
  switch(evento.keyCode){
    case teclas.DOWN:
      posY -= 2;  
      console.log("Pa' abajo weeeyyy");
    break;
    case teclas.UP: 
      posY += 2;  
      console.log("Pa' arriba");
    break;
    case teclas.RIGHT:
      posX -= 2;
      console.log("Pa' derecha");
    break;
    case teclas.LEFT:
      posX += 2;
      console.log("Pa' izquierda");
    break;
    default:
      console.log("Otra tecla");
    break
  }
  
  //Esto graba la posición en el fondo CSS
  bbb.style.backgroundPosition = posX + "px " + posY +"px";
}

function moverFondo(coorX, coorY) {
 
  posX -=  Math.floor(coorX/10);
  posY -=  Math.floor(coorY/10);

  //Esto graba la posición en el fondo CSS
  bbb.style.backgroundPosition = posX + "px " + posY +"px";
}

function init() {
  // Damos la posición al Joystick
  var xCenter = 150;
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
      $('#xVal').text('X: ' + x);
      $('#yVal').text('Y: ' + (-1 * y));
      
      var coords = calculateCoords(ev.angle, ev.distance);
      
      psp.x = coords.x;
      psp.y = coords.y;
      
      console.log("Coords.X: " + Math.floor(psp.x) + ", Coords.Y: " + Math.floor(psp.y));
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
  
function calculateCoords(angle, distance) {
    var coords = {};
    distance = Math.min(distance, 100);  
    var rads = (angle * Math.PI) / 180.0;
  
    coords.x = distance * Math.cos(rads);
    coords.y = distance * Math.sin(rads);
    
    return coords;
}