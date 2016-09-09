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
          //  socket_button.emit('click event',  $(this).attr("id")+"On");
          socket_button.emit('click event',  $(this).attr("id")+" 1");
            }
        if ($(this).attr('value') == 0)
            {
         //   socket_button.emit('click event',  $(this).attr("id")+"Off");
            socket_button.emit('click event',  $(this).attr("id")+" 0");
            }
        else
            {
         //   socket_button.emit('click event',  $(this).attr("id")+"Off");
            socket_button.emit('click event',  $(this).attr("id"));
            }
    });


    socket_button.on('datagram', function(data) {

    document.getElementById("datagram").innerHTML = data.datagram;

   if (data.datagram.indexOf("True") > -1 )
    {
    document.getElementById(data.datagram.split(" ")[0].replace(/Off$/,"").replace(/On$/,"")).className="led-green";
    }
    else if (data.datagram.indexOf("False") > -1)
    {
    document.getElementById(data.datagram.split(" ")[0].replace(/Off$/,"").replace(/On$/,"")).className="led-red";
    }
    else
    {

    }


    });


    $('[id^=Send]').submit(function () {
      socket_button.emit('click event',   $(this).find('input').attr('id') +" "+ $(this).find('input').val());
      return false;
    });


});