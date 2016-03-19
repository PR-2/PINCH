from modbus_connection import Connection as Tr
from standart_server import initialize
from standart_server import start
from standart_server import stop
from translate_apel_m_5pdc_800_2 import *


tr = Tr(indicator_list,coil_on_list,coil_off_list,command_list,"/dev/ttyUSB1")

path = "/tmp/python_unix_sockets_example"
server = initialize(path)


def read_device_function(data):
    answer = tr.translate(data)
    return answer


start(server, read_device_function)
stop(path)
