/* Cuando la página se carga, se comienzan a recuperar muestras */
$("#start-sampling").click(function(){
    console.log('Se empieza a muestrear');
    start_get_data();
});

var control_data;
function start_get_data(){
    // Establece el período de actualización cada 1 segundo
    control_data = setInterval(get_data, 1000);
}

/* Recupera los parámetros temporales de la base de datos y los dirige al navegador */
function get_data(){
    //console.log("pre-in");
    $.get("/monitor/get_data", function(data){
        //console.log("in");
        $("#last-temperature").html(data[0].temperature);
        //console.log('t1');
        $("#last-humidity").html(data[0].humidity);
        //console.log("h1");
        $("#last-pressure").html(data[0].pressure);
        //console.log("p1");
        $("#last-windspeed").html(data[0].windspeed);
        //console.log("w1");
        $("#average-temperature").html(data[1].temperature);
        //console.log("t2");
        $("#average-humidity").html(data[1].humidity);
        //console.log("h2");
        $("#average-pressure").html(data[1].pressure);
        //console.log("p2");
        $("#average-windspeed").html(data[1].windspeed);
        //console.log("w2");
    });
}

/* Interrupción de la recolección de muestras */
function stop_get_data(){
    clearInterval(control_data);
}

/* Botón que interrumpe la recuperación de muestras */
$("#stop-sampling").click(function(){    
    console.log('Se deja de muestrear');
    stop_get_data();
    //$.get("/monitor/stop");
});

/* Modificación del período de actualización de valores */
function set_refresh_interval(milliseconds){
    clearInterval(control_data);
    control_data = setInterval(milliseconds);
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