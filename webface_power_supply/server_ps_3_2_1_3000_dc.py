from modbus_connection import Connection as Tr
from standart_server import initialize
from standart_server import start
from standart_server import stop
from ps_3_2_1_3000_dc import *


tr = Tr(indicator_list, coil_on_list, coil_off_list, command_list,
        "/dev/serial/by-id/usb-ICPDAS_I-7561U_USB_Serial_Converter_00Z5PSMV-if00-port0")

path = "/tmp/python_unix_sockets_ps_3_2_1_3000"
server = initialize(path)


def read_device_function(data):
    answer = tr.translate(data)
    return answer


start(server, read_device_function)
stop(path)
