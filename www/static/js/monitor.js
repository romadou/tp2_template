/* Cuando la página se carga, se comienzan a recuperar muestras */
$(document).ready(function(){
    start_get_data();
});

var control_data;
function start_get_data(){
    // Establece el período de actualización cada 1 segundo
    control_data = setInterval(get_data, 1000);
    $("#refresh-interval").html(1);
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
}

/* Interrupción de la recolección de muestras */
function stop_get_data(){
    clearInterval(control_data);
}

/* Botón que interrumpe la recuperación de muestras */
$("#stop-sampling").click(function(){    
    stop_get_data();
    //$.get("/monitor/stop");
});

/* Modificación del período de actualización de valores */
function set_refresh_interval(milliseconds){
    clearInterval(control_data);
    control_data = setInterval(milliseconds);
}

/* Botones de selección del período de actualización de valores */
$("#button-1-sec").click(function(){    
    set_refresh_interval(1000)
    $("#refresh-interval").html(1);
});
$("#button-2-sec").click(function(){    
    set_refresh_interval(2000)
    $("#refresh-interval").html(2);
});
$("#button-5-sec").click(function(){    
    set_refresh_interval(5000)
    $("#refresh-interval").html(5);
});
$("#button-10-sec").click(function(){    
    set_refresh_interval(10000)
    $("#refresh-interval").html(10);
});
$("#button-30-sec").click(function(){    
    set_refresh_interval(30000)
    $("#refresh-interval").html(30);
});
$("#button-60-sec").click(function(){    
    set_refresh_interval(60000)
    $("#refresh-interval").html(60);
});

/* Comportamiento ante la salida no habitual de la página: finalización de la actualización de valores */
$(window).on("unload", function(e) {
    stop_get_data();
    $.get("/monitor/stop", function(data){
        console.log(data);
    });
});