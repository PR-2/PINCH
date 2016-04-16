WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
WEB_SOCKET_DEBUG = true;

var socket_button;

$(function () {
     socket_button = io.connect('/'+socket_name, {
    'reconnection': false,

});

    $('[id^=Coil]').click(function () {

        if ($(this).attr('value') == 1)
            {
            document.getElementById($(this).attr("id")).className="led-green";
            socket_button.emit('click event',  $(this).attr("id")+"On");
            }
        if ($(this).attr('value') == 0)
            {
            document.getElementById($(this).attr("id")).className="led-red";
            socket_button.emit('click event',  $(this).attr("id")+"Off");
            }
    });


    socket_button.on('datagram', function(data) {
        document.getElementById("datagram").innerHTML = data.datagram;

    });


    $('[id^=Send]').submit(function () {
      socket_button.emit('click event',   $(this).find('input').attr('id') +" "+ $(this).find('input').val());
      return false;
    });


});