WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
WEB_SOCKET_DEBUG = true;

// socket.io specific code
var socket_button;
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
     socket_button = io.connect("/button", {
    'reconnection': false,
    //'reconnection delay': 5000,
   // 'max reconnection attempts': 10
});

    $('[id^=Coil]').click(function () {
      socket_button.emit('click event',  $(this).attr('id') );
    });


    socket_button.on('datagram', function(data) {
        document.getElementById("datagram").innerHTML = data.datagram;
    });


    $('[id^=Send]').submit(function () {
      socket_button.emit('click event',   $(this).find('input').attr('id') +" "+ $(this).find('input').val());
      return false;
    });


});