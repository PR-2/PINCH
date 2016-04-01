from gevent import monkey
import gevent
from flask import Flask, Response, request, render_template
from socketio import socketio_manage
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.namespace import BaseNamespace
from connection import connect_to_server

monkey.patch_all()

app = Flask(__name__)
app.debug = True


@app.route('/capacity_changer')
def capacity_changer():
    indicator_list = "IReg_C1-value IReg_C2-value IReg_C-value IReg_Amplitude-mismatch IReg_Phase-mismatch"
    coil_list = 'Coil_AutoResistanceSetupOn  Coil_AutoResistanceSetupOff Coil_AutoReturnOn  Coil_AutoReturnOff ' \
                'Coil_EEPROM-writeOn  Coil_EEPROM-writeOff ' \
                'Coil_AutoPhaseSetupOn Coil_AutoPhaseSetupOff Coil_EngineOn Coil_EngineOff'

    command_list = "HReg_Min-C2-capacity HReg_ResistanceTuningSensitivity HReg_C-min-limit " \
                   "HReg_PhaseTuningSensitivity HReg_Max-C1-capacity HReg_InstallationAmplitudeSensorZero " \
                   "HReg_C-max-limit HReg_Max-C2-capacity HReg_Set-C2-value HReg_Set-C-value" \
                   " HReg_C2-min-limit HReg_Modbus-address HReg_Min-C1-capacity " \
                   "HReg_InstallationPhaseSensorZero HReg_C2-max-limit HReg_Threshold-auto-negotiation"

    return render_template('capacity_changer.html', indicator_list=indicator_list,
                           coil_list=coil_list, command_list=command_list)

@app.route('/rrg')
def rrg():
    indicator_list = "RRG1 RRG2 RRG3 RRG4"
    coil_list = ''
    command_list = "Set_RRG1 Set_RRG2 Set_RRG3 Set_RRG4"

    return render_template('rrg.html', indicator_list=indicator_list,
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


@app.route('/ps_3000_dc')
def ps_3000_dc():
    indicator_list = "HReg_OutputVoltage HReg_OutputCurrent HReg_Temperature "
    coil_list = ''

    command_list = "HReg_OutputVoltage HReg_WorkingTime HReg_Version HReg_Parity " \
                   "HReg_StatusFlag HReg_SetCurrent HReg_MenuLanguage HReg_TimeForWork " \
                   "HReg_Id HReg_SetVoltage HReg_Temperature HReg_RateOfDecay " \
                   "HReg_SetPower HReg_NetFlag HReg_DelayChannel HReg_InterfaceType " \
                   "HReg_Status HReg_SetStatus HReg_OutputCurrent HReg_RateOfRise " \
                   "HReg_OutputPower HReg_NetAddress HReg_ConnectionSpeed "

    return render_template('ps_3000_dc.html', indicator_list=indicator_list,
                           coil_list=coil_list, command_list=command_list)


@app.route('/gauge')
def gauge():
    gauge_list = "Gauge#1 Gauge#2"
    return render_template('gauge.html', gauge_list=gauge_list)


class GetOutOfLoop(Exception):
    pass


class Read_data(BaseNamespace, BroadcastMixin):
    command_list = "IReg_State IReg_Voltage IReg_Current IReg_Power IReg_Sec IReg_Min IReg_Hour"
    socket_name = "/tmp/python_unix_sockets_example"
    emit_path = 'ask_data'

    def recv_connect(self):

        def ask_for_data():

            while True:

                try:

                    for command in self.command_list.split():
                        msg = command + "_ask" + " = "
                       # print msg
                        datagram = connect_to_server(self.socket_name, None, msg)
                      #  print datagram
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


class Read_Capacity(Read_data):
    command_list = "IReg_C1-value IReg_C2-value IReg_C-value " \
                   "IReg_Amplitude-mismatch IReg_Phase-mismatch"
    socket_name = "/tmp/python_unix_sockets_capacity"
    emit_path = 'ask_data_cap'

class Read_Rrg(Read_data):
    command_list = "RRG1 RRG2 RRG3 RRG4"
    socket_name = "/tmp/python_unix_sockets_rrg"
    emit_path = 'ask_data_rrg'

class Read_PS(Read_data):
    command_list = "HReg_OutputVoltage HReg_OutputCurrent HReg_Temperature "
    socket_name = "/tmp/python_unix_sockets_ps_3_2_1_3000"
    emit_path = 'ask_data_ps'


class Read_Gauge(Read_data):
    command_list = "Gauge1 Gauge2"
    socket_name = "/tmp/python_unix_sockets_gauge"
    emit_path = 'ask_gauge'


class Button(BaseNamespace, RoomsMixin, BroadcastMixin):
    def recv_connect(self):
        pass

    def recv_disconnect(self):
        self.disconnect(silent=True)

        return True

    def on_click_event(self, msg):
        datagram = connect_to_server("/tmp/python_unix_sockets_example", "./log.txt", msg)

        self.emit('datagram', {'datagram': datagram})


class Button_Capacity(Button):
    def on_click_event(self, msg):
        datagram = connect_to_server("/tmp/python_unix_sockets_capacity", "./log.txt", msg)

        self.emit('datagram', {'datagram': datagram})

class Button_Rrg(Button):
    def on_click_event(self, msg):
        datagram = connect_to_server("/tmp/python_unix_sockets_rrg", "./log.txt", msg)

        self.emit('datagram', {'datagram': datagram})

class Button_PS(Button):
    def on_click_event(self, msg):
        datagram = connect_to_server("/tmp/python_unix_sockets_ps_3_2_1_3000", "./log.txt", msg)

        self.emit('datagram', {'datagram': datagram})


@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
    try:
        socketio_manage(request.environ, {'/ask_data': Read_data, '/button': Button, '/ask_gauge': Read_Gauge,
                                          '/ask_data_cap': Read_Capacity, '/button_cap': Button_Capacity,
                                          '/ask_data_rrg': Read_Rrg, '/button_rrg': Button_Rrg,
                                          '/ask_data_ps': Read_PS, '/button_ps': Button_PS})


    except:
        app.logger.error("Exception while handling socketio connection",
                         exc_info=True)
    return Response()


if __name__ == '__main__':
    app.run()
