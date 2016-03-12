import os
import os.path
import socket


from PfeifferVacuum_Gauge import MaxiGauge, MaxiGaugeError

import sys

mg = MaxiGauge('/dev/ttyUSB1', 2)

if os.path.exists("/tmp/python_unix_sockets_gauge"):
    os.remove("/tmp/python_unix_sockets_gauge")

print "Opening socket..."
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind("/tmp/python_unix_sockets_gauge")
server.listen(1)
server.settimeout(1)
# start()

print "Listening..."
while True:
    try:
        # Wait for a connection
        # print >>sys.stderr, 'waiting for a connection'
        connection, client_address = server.accept()
        # connection.setblocking(0)
        try:
            # print >>sys.stderr, 'connection from', client_address

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(256)
               # print >> sys.stderr, 'received "%s"' % data
                # check(data)
                if data:
                     try:
                        ps = mg.pressures()
                     except MaxiGaugeError, mge:
                        print mge

                     line = ""
                     gauges = {
                         "Gauge#1": 0,
                         "Gauge#2": 1}

                     sensor= ps[gauges[data.split()[0]]]
                   #  print sensor

                            #print sensor values
                     if sensor.status in [0,1,2]: # if normal, over or under range
                        line += str(sensor.pressure)

                   #  print line # omit the last comma and space
                     sys.stdout.flush()
                     answer = line
                     print answer


                    #  print >>sys.stderr, 'sending data back to the client'
                     connection.sendall(data + " " + str(answer))  # + " received from server")

                else:
                    # print >>sys.stderr, 'no more data from', client_address
                    break


        except:
            connection.close()
            print "Error"
    except:
        pass
# stop()
os.remove("/tmp/python_unix_sockets_gauge")
print "Shutting down..."
# server.close()



