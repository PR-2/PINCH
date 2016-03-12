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


@app.route('/')
def rooms():
    indicator_list = "IReg_State IReg_Voltage IReg_Current IReg_Power IReg_Sec IReg_Min IReg_Hour"
    coil_list = 'Coil_ON Coil_OFF Coil_StTimerON Coil_StTimerOFF Coil_RstTimer Coil_IgnOn Coil_IgnOff ' \
                'Coil_OutSwitch_A Coil_OutSwitch_B'
    command_list = "HReg_StabMode HReg_Voltage HReg_Current HReg_Power HReg_Mode HReg_Freq HReg_DCyo " \
                   "HReg_Sec Send_HReg_Min HReg_Hour HReg_RemCtrl HReg_ArcCnt"

    return render_template('index.html', indicator_list=indicator_list,
                           coil_list=coil_list, command_list=command_list)


@app.route('/gauge')
def gauge():
    gauge_list = "Gauge#1 Gauge#2"
    return render_template('gauge.html', gauge_list=gauge_list)


class GetOutOfLoop(Exception):
    pass


class Read_data(BaseNamespace, BroadcastMixin):
    def recv_connect(self):

        def ask_for_data():

            while True:

                try:

                    command_list = "IReg_State IReg_Voltage IReg_Current IReg_Power IReg_Sec IReg_Min IReg_Hour"
                    for command in command_list.split():
                        msg = command + "_ask" + " = "
                        datagram = connect_to_server("/tmp/python_unix_sockets_example", None, msg)
                        self.emit('ask_data', {'datagram': datagram})

                    gevent.sleep(0.01)
                except:
                    break

        self.ask_data = self.spawn(ask_for_data)

    def get_initial_acl(self):
        super(Read_data, self).get_initial_acl()

    def recv_disconnect(self):

        gevent.kill(self.ask_data)
        self.jobs = []

        return True


class Read_Gauge(BaseNamespace, BroadcastMixin):
    lock = threading.Lock()

    n = 0

    def recv_connect(self):

        def ask_gauge():

            while True:

                command_list = "Gauge#1,Gauge#2"
                for command in command_list.split(","):
                    msg = command + "_ask" + " = "

                    datagram = connect_to_server("/tmp/python_unix_sockets_gauge", None, msg)

                    self.emit('ask_gauge', {'datagram': datagram})

                gevent.sleep(0.01)

        self.ask = self.spawn(ask_gauge)
        gevent.sleep(0.01)

    def get_initial_acl(self):
        super(Read_Gauge, self).get_initial_acl()

    def recv_disconnect(self):

        gevent.kill(self.ask)
        self.jobs = []

        return True


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


class Button(BaseNamespace, RoomsMixin, BroadcastMixin):
    def recv_connect(self):
        pass

    def recv_disconnect(self):
        self.disconnect(silent=True)

        return True

    def on_click_event(self, msg):
        datagram = connect_to_server("/tmp/python_unix_sockets_example", "./log.txt", msg)

        self.emit('datagram', {'datagram': datagram})


@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
    try:
        socketio_manage(request.environ, {'/ask_data': Read_data, '/button': Button, '/ask_gauge': Read_Gauge})


    except:
        app.logger.error("Exception while handling socketio connection",
                         exc_info=True)
    return Response()


if __name__ == '__main__':
    app.run()
