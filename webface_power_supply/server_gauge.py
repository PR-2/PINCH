import os
import os.path
import socket
import sys

from PfeifferVacuum_Gauge import MaxiGauge, MaxiGaugeError

mg = MaxiGauge('/dev/ttyUSB1', 2)

if os.path.exists("/tmp/python_unix_sockets_gauge"):
    os.remove("/tmp/python_unix_sockets_gauge")

print "Opening socket..."
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind("/tmp/python_unix_sockets_gauge")
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
                try:
                    ps = mg.pressures()
                except MaxiGaugeError, mge:
                    print mge

                line = ""
                gauges = {
                    "Gauge#1": 0,
                    "Gauge#2": 1}

                sensor = ps[gauges[data.split()[0]]]

                if sensor.status in [0, 1, 2]:
                    line += str(sensor.pressure)

                sys.stdout.flush()
                answer = line
                values[data.split()[0]] = str(answer)

                connection.sendall(data + " " + str(answer))
            else:

                for name, value in values.iteritems():

                    if data.split("_")[0] == name:
                        connection.sendall(name + " = " + value)

            connection.close()
        except:
            pass




    except:
        pass

os.remove("/tmp/python_unix_sockets_gauge")
print "Shutting down..."
