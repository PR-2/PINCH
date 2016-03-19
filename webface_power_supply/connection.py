import datetime
import os
import socket


def connect_to_server(socket_file, log_file, msg,
                      socket_param_1=socket.AF_UNIX, socket_param_2=socket.SOCK_STREAM):
    if log_file:
        with open(log_file, 'a') as f:
            f.write(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " button " + str(
                msg) + " pressed" + "\n")
    try:
        if os.path.exists(socket_file):
            client = socket.socket(socket_param_1, socket_param_2)

            client.settimeout(0.2)
            client.connect(socket_file)
            client.settimeout(None)

            client.send(msg)
            datagram = client.recv(256)

            client.close()
            return datagram
    except:
        return "No Data"
