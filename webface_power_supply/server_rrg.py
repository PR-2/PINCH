import RRG
from standart_server import initialize
from standart_server import start
from standart_server import stop

port = "/dev/ttyUSB0"

RRG1 = {'input': 3, 'output': 0}
RRG2 = {'input': 5, 'output': 1}
RRG3 = {'input': 6, 'output': 2}
RRG4 = {'input': 9, 'output': 3}

rrg = [RRG1, RRG2, RRG3, RRG4]
gas = RRG.RRG(port, rrg)

path = "/tmp/python_unix_sockets_rrg"
server = initialize(path)


def read_device_function(data):

    print data
    answer = "No data"
    if "Set_" in data:
        device = rrg[int(data.split("_")[1][3]) - 1]
        if len(data.split()) > 1:
            answer = str(gas.write(device, float(data.split()[1])))

    else:
        device = rrg[int(data[3]) - 1]
        answer = "{:.2f}".format(gas.read(device))
    print answer

    return answer


start(server, read_device_function)
stop(path)
gas.close()