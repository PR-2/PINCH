import os
import socket


def initialize(path, socket_param_1=socket.AF_UNIX, socket_param_2=socket.SOCK_STREAM):
    if os.path.exists(path):
        os.remove(path)

    print "Opening socket..."
    server = socket.socket(socket_param_1, socket_param_2)
    server.bind(path)
    server.listen(2)
    server.settimeout(1)

    print "Listening..."
    return server


def start(server, read_device_function):
    values = {}

    while True:
        try:

            connection, client_address = server.accept()

            try:

                data = connection.recv(256)

                if ("ask" not in data):

                    answer = read_device_function(data)

                    values[data.split()[0]] = str(answer)

                    connection.sendall(data + " " + str(answer))
                else:

                    for name, value in values.iteritems():

                        if data[:-7] == name:
                            connection.sendall(name + " = " + value)

                connection.close()


            except:

                print "Error"
        except:
            pass


def stop(path):
    os.remove(path)
    print "Shutting down..."
