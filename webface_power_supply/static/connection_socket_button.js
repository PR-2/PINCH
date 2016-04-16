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
            socket_button.emit('click event',  $(this).attr("id")+"On");
            }
        if ($(this).attr('value') == 0)
            {
            socket_button.emit('click event',  $(this).attr("id")+"Off");
            }
    });


    socket_button.on('datagram', function(data) {

    document.getElementById("datagram").innerHTML = data.datagram;

   if (data.datagram.split(" ")[1] == "True"){

    document.getElementById(data.datagram.split(" ")[0].replace(/Off$/,"").replace(/On$/,"")).className="led-green";
    }
    else if (data.datagram.split(" ")[1] == "False")
    {
    document.getElementById(data.datagram.split(" ")[0].replace(/Off$/,"").replace(/On$/,"")).className="led-red";
    }
    else
    {
    alert("Что-то пошло не так =(");
    }


    });


    $('[id^=Send]').submit(function () {
      socket_button.emit('click event',   $(this).find('input').attr('id') +" "+ $(this).find('input').val());
      return false;
    });


});