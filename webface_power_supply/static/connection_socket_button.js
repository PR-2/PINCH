WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
WEB_SOCKET_DEBUG = true;


var socket_button;


$(function () {
     socket_button = io.connect("/button", {
    'reconnection': false,

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