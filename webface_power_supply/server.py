import os
import os.path
import socket

from translate_apel_m_5pdc_800_2 import Connection_to_power_supply as Tr

tr = Tr()

if os.path.exists("/tmp/python_unix_sockets_example"):
    os.remove("/tmp/python_unix_sockets_example")

print "Opening socket..."
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind("/tmp/python_unix_sockets_example")
server.listen(2)
server.settimeout(1)

values = {}
print "Listening..."
while True:
    try:

        connection, client_address = server.accept()

        try:

            data = connection.recv(256)

            if ("ask" not in data):

                answer = tr.translate("/dev/ttyUSB0", data)

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
os.remove("/tmp/python_unix_sockets_example")
print "Shutting down..."
