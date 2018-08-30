/* Cuando la página se carga, se comienzan a recuperar muestras */
$("#start-sampling").click(function(){
    console.log('Se empieza a muestrear');
    start_get_data();
});

var milliseconds = 1000;
var refresh_time = 0;
var refresh_control;

function start_get_data(){
    // Establece el período de actualización cada 1 segundo
    refresh_time = 1;    
    refresh_control = setTimeout(get_data, milliseconds);
}


/* Recupera los parámetros temporales de la base de datos y los dirige al navegador */
function get_data(){
    $.get("/monitor/get_data", function(data){
        $("#last-temperature").html(data[0].temperature);
        $("#last-humidity").html(data[0].humidity);
        $("#last-pressure").html(data[0].pressure);
        $("#last-windspeed").html(data[0].windspeed);
        $("#average-temperature").html(data[1].temperature);
        $("#average-humidity").html(data[1].humidity);
        $("#average-pressure").html(data[1].pressure);
        $("#average-windspeed").html(data[1].windspeed);
    });
    refresh_control = setTimeout(get_data, milliseconds);
}

/* Interrupción de la actualización de muestras en pantalla */
function stop_get_data(){
    refresh_time = 0;
    clearTimeout(refresh_control);
}

/* Botón que interrumpe la recuperación de muestras al browser */
$("#stop-sampling").click(function(){    
    console.log('Se deja de muestrear');
    stop_get_data();
});

/* Modificación del período de actualización de valores */
function set_refresh_interval(ms){
    milliseconds = ms;
}

/* Botones de selección del período de actualización de valores */
$("#1-second").click(function(){    
    set_refresh_interval(1000)
});
$("#2-seconds").click(function(){    
    set_refresh_interval(2000)
});
$("#5-seconds").click(function(){    
    set_refresh_interval(5000)
});
$("#10-seconds").click(function(){    
    set_refresh_interval(10000)
});
$("#30-seconds").click(function(){    
    set_refresh_interval(30000)
});
$("#60-seconds").click(function(){    
    set_refresh_interval(60000)
});

/* Comportamiento ante la salida no habitual de la página: finalización de la actualización de valores */
$(window).on("unload", function(e) {
    stop_get_data();
    $.get("/monitor/stop", function(data){
        console.log(data);
    });
});
