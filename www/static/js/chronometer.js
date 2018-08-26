var segundos = 0;
var minutos = 0;
var horas = 0;
var control_chrono;

$(document).ready(function(){
    start_chrono();
});

function start_chrono() {
    control_chrono = setInterval(chronometro, 1000);
}

function stop_chrono() {
    clearInterval(control_chrono);            
}

function chronometro() {
    if (segundos < 59) {
        segundos++;
        if (segundos < 10) { segundos = "0"+segundos }
    }
    if (segundos == 59) {
        segundos = -1;
    }
    if ( (centesimas == 0)&&(segundos == 0) ) {
        minutos++;
        if (minutos < 10) { minutos = "0"+minutos }
    }
    if (minutos == 59) {
        minutos = -1;
    }
    if ( (segundos == 0) && (minutos == 0) ) {
        horas++;
        if (horas < 10) { horas = "0"+horas }             
    }
}