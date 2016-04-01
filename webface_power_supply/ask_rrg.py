import gevent

from connection import connect_to_server

while True:

    command_list = "RRG1,RRG2,RRG3,RRG4"
    for command in command_list.split(","):
        msg = command + " = "
        datagram = connect_to_server("/tmp/python_unix_sockets_rrg", None, msg)
        gevent.sleep(0.01)
