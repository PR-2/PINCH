import gevent

from connection import connect_to_server

while True:

    command_list = "Gauge1,Gauge2"
    for command in command_list.split(","):
        msg = command + " = "
        datagram = connect_to_server("/tmp/python_unix_sockets_gauge", None, msg)
        gevent.sleep(0.5)
