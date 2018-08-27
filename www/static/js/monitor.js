/*
    Functions:
        $(document).ready(function(){});
        start_get_data()
        get_data() (calling /monitor with a GET)
            (problem with two different /monitor??)
            LEARN HOW TO !!FIRST RENDER!! THEN REFRESH VALUES
        stop_get_data()
        set_refresh_interval() (button and HTML-response for this)
    IDs:
        #last-<values>
        #average-<values>
        #refresh_interval -> maybe not necessary if there are different button, not a toggle box
*/

$(document).ready(function(){

    // TODO: maybe not a post, but a get; since is first instance, GET from /monitor won't get data
    // TODO: this MUST call monitor.html render with initial values
    // $.post("/monitor", function(data){

    // })

    start_get_data();

});


var control_data;
function start_get_data(){
    // Sets refresh period every 1 second
    control_data = setInterval(get_data, 1000);
}

function get_data(){
    $.get("/monitor", function(data){
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

function stop_get_data(){
    clearInterval(control_data);
}

$("#stop-sampling").click(function(){    
    stop_get_data();
    $.get("/monitor/stop");
});

// TODO: implement response to HTML element (guess it'll be different if toggle box or separate buttons)
function set_refresh_interval(milliseconds){
    clearInterval(control_data);
    control_data = setInterval(milliseconds);
}


// $(document).ready(function() {

//     $.get("/team/" + id_team_west, function(data) {
//         $('#logo-' + id_team_west).attr('src', "data:image/png;base64," + data.logo);
//         $("#name-" + id_team_west).html(data.name);
//     });

//     $.get("/team/" + id_team_east, function(data) {
//         $('#logo-' + id_team_east).attr('src', "data:image/png;base64," + data.logo);
//         $("#name-" + id_team_east).html(data.name);
//     });

//     start_get_score();

//     $('#modal-result').modal({backdrop: 'static', keyboard: false, show:false});
// });

// $(window).on("unload", function(e) {
//     $.get("/match/stop/" + id_match, function(data){
//         console.log(data);
//     });
// });

// var control_score;

// function start_get_score() {
//     control_score = setInterval(score, 2000);
// }

// function stop_get_score() {
//     clearInterval(control_score);
//     stop_chrono();
// }

// function score() {
//     $.get("/result/match/" + id_match, function(data) {
//         $("#score-" + data[0].id_team).html(data[0].score);
//         $("#score-" + data[1].id_team).html(data[1].score);
//     });
// }

// $("#stop-match").click(function() {    
//     stop_get_score();
//     $.get("/match/stop/" + id_match, function(data) {
//         console.log(data);
//     }).done(function() {        
//         $.get("/result/match/" + id_match, function(data) {
//             $("#score-" + data[0].id_team).html(data[0].score);
//             $("#score-" + data[1].id_team).html(data[1].score);
//             var id_team_result = (data[0].score > data[1].score) ? data[0].id_team : (data[1].score > data[0].score) ? data[1].id_team : null;
//             var text = (id_team_result == null) ? "The match ended tied" : "The winner is " + $('#name-' + id_team_result).html();
//             $("#text-result").html(text);
//             $('#modal-result').modal('show');
//         });
//     });
// });