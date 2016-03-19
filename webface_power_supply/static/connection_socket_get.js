
WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
WEB_SOCKET_DEBUG = true;

var socket ;

$(function() {
socket = io.connect('/'+socket_ask_name,{
    'reconnect': false

});

socket.on(socket_ask_name, function(data) {
    document.getElementById(data.datagram.split(" ")[0]).innerHTML = data.datagram;
    document.getElementById("value").innerHTML = data.datagram.split(" ")[0];


});

});