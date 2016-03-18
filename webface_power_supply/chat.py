from gevent import monkey

monkey.patch_all()

import gevent
import datetime
import os
import os.path
import socket


from flask import Flask, Response, request, render_template

from socketio import socketio_manage
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.namespace import BaseNamespace

app = Flask(__name__)
app.debug = True


@app.route('/capacity_changer')
def capacity_changer():
    indicator_list = "IReg_C1-value IReg_C2-value IReg_C-value IReg_Amplitude-mismatch IReg_Phase-mismatch"
    coil_list = 'Coil_AutoResistanceSetupOn Coil_AutoReturnOn Coil_EEPROM-writeOn ' \
                'Coil_AutoPhaseSetupOn Coil_EngineOn ' \
                 'Coil_AutoPhaseSetupOff Coil_AutoResistanceSetupOff Coil_EEPROM-writeOff ' \
                 'Coil_EngineOff Coil_AutoReturnOff'

    command_list = "HReg_Min-C2-capacity HReg_ResistanceTuningSensitivity HReg_C-min-limit " \
                   "HReg_PhaseTuningSensitivity HReg_Max-C1-capacity HReg_InstallationAmplitudeSensorZero " \
                   "HReg_C-max-limit HReg_Max-C2-capacity HReg_Set-C2-value HReg_Set-C-value" \
                   " HReg_C2-min-limit HReg_Modbus-address HReg_Min-C1-capacity " \
                   "HReg_InstallationPhaseSensorZero HReg_C2-max-limit HReg_Threshold-auto-negotiation"

    return render_template('capacity_changer.html', indicator_list=indicator_list,
                           coil_list=coil_list, command_list=command_list)


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




class Read_data (BaseNamespace, BroadcastMixin):
    command_list = "IReg_State IReg_Voltage IReg_Current IReg_Power IReg_Sec IReg_Min IReg_Hour"
    socket_name = "/tmp/python_unix_sockets_example"
    emit_path= 'ask_data'

    def recv_connect(self):

        def ask_for_data():

            while True:

                try:


                    for command in self.command_list.split():
                        msg = command + "_ask" + " = "
                        print msg
                        datagram = connect_to_server(self.socket_name, None, msg)
                        print datagram
                        self.emit(self.emit_path, {'datagram': datagram})


                    gevent.sleep(1)
                except:
                    break

        self.ask_data = self.spawn(ask_for_data)

    def get_initial_acl(self):
        super(Read_data, self).get_initial_acl()

    def recv_disconnect(self):

        gevent.kill(self.ask_data)
        self.jobs = []

        return True

class Read_Capacity( Read_data):
    command_list = "IReg_C1-value IReg_C2-value IReg_C-value " \
                   "IReg_Amplitude-mismatch IReg_Phase-mismatch"
    socket_name = "/tmp/python_unix_sockets_capacity"
    emit_path = 'ask_data_cap'



class Read_Gauge( Read_data):
    command_list = "Gauge#1 Gauge#2"
    socket_name = "/tmp/python_unix_sockets_gauge"
    emit_path ='ask_gauge'



class Button(BaseNamespace, RoomsMixin, BroadcastMixin):
    def recv_connect(self):
        pass

    def recv_disconnect(self):
        self.disconnect(silent=True)

        return True

    def on_click_event(self, msg):
        datagram = connect_to_server("/tmp/python_unix_sockets_example", "./log.txt", msg)

        self.emit('datagram', {'datagram': datagram})

class Button_Capacity( Button):

    def on_click_event(self, msg):
        datagram = connect_to_server("/tmp/python_unix_sockets_capacity", "./log.txt", msg)

        self.emit('datagram', {'datagram': datagram})




@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
    try:
        socketio_manage(request.environ, {'/ask_data': Read_data, '/button': Button, '/ask_gauge': Read_Gauge,
                                          '/ask_data_cap': Read_Capacity, '/button_cap': Button_Capacity})


    except:
        app.logger.error("Exception while handling socketio connection",
                         exc_info=True)
    return Response()


if __name__ == '__main__':
    app.run()
