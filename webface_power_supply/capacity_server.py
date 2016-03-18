import os
import os.path
import socket

from capacity_changer import Connection_to_capacity_changer as Tr

tr = Tr()

if os.path.exists("/tmp/python_unix_sockets_capacity"):
    os.remove("/tmp/python_unix_sockets_capacity")

print "Opening socket..."
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind("/tmp/python_unix_sockets_capacity")
server.listen(2)
server.settimeout(1)

values = {}
print "Listening... start"
while True:
    try:

        connection, client_address = server.accept()

        try:

            data = connection.recv(256)
            print values


            if ("_ask " not in data):
                print "123"
                answer = tr.translate("/dev/ttyUSB0", data)

                print int(answer)

                values[data.split()[0]] = str(answer)

                connection.sendall(data + " " + str(answer))
            else:
                print "!!!456"
                for name, value in values.iteritems():

                    if data[:-7] == name:
                        connection.sendall(name + " = " + value)

            connection.close()


        except:

            print "Error"
    except:
        pass
os.remove("/tmp/python_unix_sockets_capacity")
print "Shutting down..."
