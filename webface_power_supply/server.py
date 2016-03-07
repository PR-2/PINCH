import os
import os.path
import socket

from translate_apel_m_5pdc_800_2 import Connection_to_power_supply as Tr
# from message_serial import stop, start, check
import sys

tr = Tr()

if os.path.exists("/tmp/python_unix_sockets_example"):
    os.remove("/tmp/python_unix_sockets_example")

print "Opening socket..."
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind("/tmp/python_unix_sockets_example")
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
                print >> sys.stderr, 'received "%s"' % data
                # check(data)
                if data:

                    answer = tr.translate("/dev/ttyUSB1", data)
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
os.remove("/tmp/python_unix_sockets_example")
print "Shutting down..."
# server.close()



