import gevent

from connection import connect_to_server
n = True
while True:
    if n:
        command_list = "HReg_OutputVoltage HReg_WorkingTime HReg_Version HReg_Parity " \
                   "HReg_StatusFlag HReg_SetCurrent HReg_MenuLanguage HReg_TimeForWork " \
                   "HReg_Id HReg_SetVoltage HReg_Temperature HReg_RateOfDecay " \
                   "HReg_SetPower HReg_NetFlag HReg_DelayChannel HReg_InterfaceType " \
                   "HReg_Status HReg_SetStatus HReg_OutputCurrent HReg_RateOfRise " \
                   "HReg_OutputPower HReg_NetAddress HReg_ConnectionSpeed "
    else:
        command_list = "HReg_OutputVoltage HReg_OutputCurrent " \
                       "HReg_Temperature "


    for command in command_list.split():
        msg = command + " = "
        datagram = connect_to_server("/tmp/python_unix_sockets_ps_3_2_1_3000", None, msg)

        gevent.sleep(0.01)
    n = False
