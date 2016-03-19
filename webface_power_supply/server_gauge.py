import sys

from PfeifferVacuum_Gauge import MaxiGauge, MaxiGaugeError
from standart_server import initialize
from standart_server import start
from standart_server import stop

mg = MaxiGauge('/dev/ttyUSB1', 2)
path = "/tmp/python_unix_sockets_gauge"
server = initialize(path)


def read_device_function(data):
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
    return answer


start(server, read_device_function)
stop(path)
