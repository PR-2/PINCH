import gevent

from connection import connect_to_server

while True:

    command_list = "IReg_State IReg_Voltage IReg_Current IReg_Power IReg_Sec IReg_Min IReg_Hour"
    for command in command_list.split():
        msg = command + " = "
        datagram = connect_to_server("/tmp/python_unix_sockets_example", None, msg)

        gevent.sleep(0.01)
