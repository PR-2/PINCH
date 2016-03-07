from gevent import monkey
monkey.patch_all()

import gevent
import datetime
import os
import os.path
import socket
import threading

from flask import Flask, Response, request, render_template

from socketio import socketio_manage
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.namespace import BaseNamespace



app = Flask(__name__)
app.debug = True


# views
@app.route('/')
def rooms():
    """
    Homepage - lists all rooms.
    """
    indicator_list = "IReg_State IReg_Voltage IReg_Current IReg_Power IReg_Sec IReg_Min IReg_Hour"
    coil_list = 'Coil_ON Coil_OFF Coil_StTimerON Coil_StTimerOFF Coil_RstTimer Coil_IgnOn Coil_IgnOff ' \
                'Coil_OutSwitch_A Coil_OutSwitch_B'
    command_list = "HReg_StabMode HReg_Voltage HReg_Current HReg_Power HReg_Mode HReg_Freq HReg_DCyo " \
                   "HReg_Sec Send_HReg_Min HReg_Hour HReg_RemCtrl HReg_ArcCnt"

    return render_template('index.html', indicator_list=indicator_list,
                           coil_list=coil_list,command_list=command_list)


@app.route('/gauge')
def gauge():
    gauge_list = "Gauge#1 Gauge#2"
    return render_template('gauge.html', gauge_list=gauge_list)


class GetOutOfLoop(Exception):
    pass


class Read_data(BaseNamespace, BroadcastMixin):
    lock = threading.Lock()

    # lock.acquire()



    def recv_connect(self):

        def ask_for_data():
            # prev = None
            # gevent.sleep(3)


            self.lock.acquire()
            print str(self.lock) + "  CONNECT  " + str(self.lock.locked())
            while self.lock.locked():

                try:

                    # print "START LOOP"
                    # vals = psutil.cpu_percent(interval=1, percpu=True)
                    command_list = "IReg_State IReg_Voltage IReg_Current IReg_Power IReg_Sec IReg_Min IReg_Hour"
                    for command in command_list.split():
                        msg = command + " = "  # + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                        # print str(self.lock) + "  STatus  " + str(self.lock.locked())
                        datagram = connect_to_server("/tmp/python_unix_sockets_example", None, msg)

                        print msg
                        # answer = tr.translate("/dev/ttyUSB0",msg)
                        # datagram = msg + " " + str(answer)
                       # print datagram
                        #  print >>sys.stderr, 'sending data back to the client'
                        # connection.sendall( data + " " + str(answer) )#+ " received from server")

                        # if prev:
                        #    percent = (sum(vals) - sum(prev))
                        self.emit('ask_data', {'datagram': datagram})
                        if not self.lock.locked():
                            print "FINISH LOOP"
                            raise GetOutOfLoop

                    # prev = vals
                    gevent.sleep(0.001)
                except :
                    break

        self.ask_data = self.spawn(ask_for_data)


    def get_initial_acl(self):
        super(Read_data, self).get_initial_acl()

    def recv_disconnect(self):
        # Remove nickname from the list 

        print "!!!DISCONNECT123!!! start"
        self.lock.release()

        print str(self.lock) + "  DISCONNECT  " + str(self.lock.locked())
        print self.jobs
        print self.ask_data

        gevent.kill(self.ask_data)
        self.jobs = []
        print self.ask_data
       # self.lock.release()
        print "!!!DISCONNECT123!!! stop"
        #self.disconnect()

        # datagram = connect_to_server("/tmp/python_unix_sockets_example","./log.txt","")
        return True
        # client.close()




class Read_Gauge(BaseNamespace, BroadcastMixin):
   # __metaclass__ = Singleton
    lock = threading.Lock()


    n = 0
    def recv_connect(self):

                #gevent.kill(self.jobs[self.jobs.index(job)])


        def ask_gauge():
            # prev = None
            # gevent.sleep(3)


            #self.lock.acquire()
         #   print str(self.lock) + "  CONNECT  " + str(self.lock.locked())
           # while self.lock.locked():
            while True:

                    self.n+=1
                    print str(self.n) + " !!!!!calc"
                    # print "START LOOP"
                    # vals = psutil.cpu_percent(interval=1, percpu=True)
                    command_list = "Gauge#1,Gauge#2"
                    for command in command_list.split(","):
                        msg = command + " = "  # + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                        # print str(self.lock) + "  STatus  " + str(self.lock.locked())
                        datagram = connect_to_server("/tmp/python_unix_sockets_gauge", None, msg)

                        print datagram

                        self.emit('ask_gauge', {'datagram': datagram})
                        #if not self.lock.locked():
                       #     print "FINISH LOOP"
                       #     raise GetOutOfLoop
                   #     datagram1 = listen_to_server("/tmp/python_unix_sockets_gauge", None, msg)
                      #  print "!!!!!"+str(datagram1)+"!!!!!"

                    # prev = vals
                    gevent.sleep(0.001)





        self.ask = self.spawn(ask_gauge)
        gevent.sleep(0.01)



    def get_initial_acl(self):
        super(Read_Gauge, self).get_initial_acl()

    def recv_disconnect(self):
        # Remove nickname from the list
        #self.lock.release()

        print self.jobs
        print self.ask
        print "!!!DISCONNECT!!! start"





        #11print str(self.lock) + "  DISCONNECT  " + str(self.lock.locked())
        try:
          #  self.disconnect()

            gevent.kill(self.ask)
            self.jobs = []
            print "LOOOL"
        except Exception as e:
            print "HUITA", e
        print str(self.jobs)+ "!!!"
        print "!!!DISCONNECT!!! stop"


        # datagram = connect_to_server("/tmp/python_unix_sockets_example","./log.txt","")
        return True
        # client.close()


def connect_to_server(socket_file, log_file, msg):
    # print "Connecting to socket..."
    # log_file="./log.txt"
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
            # print datagram
            client.close()
            return datagram
    except:
        return "No Data"

###############################################################
# def listen_to_server(socket_file, log_file, msg):
#     # print "Connecting to socket..."
#     # log_file="./log.txt"
#     if log_file:
#         with open(log_file, 'a') as f:
#             f.write(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " button " + str(
#                 msg) + " pressed" + "\n")
#     try:
#         if os.path.exists(socket_file):
#             client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#             client.settimeout(0.2)
#             client.connect(socket_file)
#             client.settimeout(None)
#            # client.send(msg)
#             datagram = client.recv(256)
#             # print datagram
#             client.close()
#             return datagram
#     except:
#         return None
###############################################################

class Button(BaseNamespace, RoomsMixin, BroadcastMixin):
    def recv_disconnect(self):
        # Remove nickname from the list       
        self.disconnect(silent=True)

        # datagram = connect_to_server("/tmp/python_unix_sockets_example","./log.txt","")
        return True
        # client.close()

    def on_click_event(self, msg):
        datagram = ""
        datagram = connect_to_server("/tmp/python_unix_sockets_example", "./log.txt", msg)
        # answer = tr.translate("/dev/ttyUSB0",msg)
        # datagram = msg + " " + str(answer)
        self.emit('datagram', {'datagram': datagram})

        #  print >>sys.stderr, 'sending data back to the client'
        # connection.sendall( data + " " + str(answer) )#+ " received from server")

        # def recv_message(self, message):
        #     print "PING!!!", message



@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
    try:
        socketio_manage(request.environ, {'/ask_data': Read_data, '/button': Button,'/ask_gauge': Read_Gauge})


    except:
        app.logger.error("Exception while handling socketio connection",
                         exc_info=True)
    return Response()


if __name__ == '__main__':
    app.run()
