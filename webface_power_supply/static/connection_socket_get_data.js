
WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
WEB_SOCKET_DEBUG = true;

var socket ;

$(function() {
socket =  io.connect('/ask_data',{
    'reconnect': false

});

socket.on('ask_data', function(data) {
    document.getElementById(data.datagram.split(" ")[0]).innerHTML = data.datagram;

});

});