WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
WEB_SOCKET_DEBUG = true;

// socket.io specific code
var socket = io.connect("/button", {
    'reconnection': false,
    //'reconnection delay': 5000,
   // 'max reconnection attempts': 10
});

/*$(window).bind("beforeunload", function() {
    socket.disconnect();
});

socket.on('connect', function () {
    $('#main').addClass('connected');
});


socket.on('disconnect', function () {
    setTimeout(function () {
         //do something
    }, 10000);
});*/

// DOM manipulation
$(function () {


    $('[id^=Coil]').click(function () {
      socket.emit('click event',  $(this).attr('id') );
    });


    socket.on('datagram', function(data) {
        document.getElementById("datagram").innerHTML = data.datagram;
    });


    $('[id^=Send]').submit(function () {
      socket.emit('click event',   $(this).find('input').attr('id') +" "+ $(this).find('input').val());
      return false;
    });


});