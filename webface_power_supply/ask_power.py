import datetime
import os
import socket

import gevent


def connect_to_server(socket_file, log_file, msg):
    if log_file:
        with open(log_file, 'a') as f:
            f.write(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " button " + str(
                msg) + " pressed" + "\n")
    try:
        if os.path.exists(socket_file):
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.settimeout(0.2)
            client.connect(socket_file)
            client.settimeout(None)
            client.send(msg)
            datagram = client.recv(256)
            client.close()
            return datagram
    except:
        return "No Data"


while True:

    command_list = "IReg_State IReg_Voltage IReg_Current IReg_Power IReg_Sec IReg_Min IReg_Hour"
    for command in command_list.split():
        msg = command + " = "
        datagram = connect_to_server("/tmp/python_unix_sockets_example", None, msg)

    gevent.sleep(0.001)
