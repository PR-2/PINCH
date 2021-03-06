import RRG
from standart_server import initialize
from standart_server import start
from standart_server import stop

port = "/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0"


RRG1 = {'input': 3, 'output': 0, 'open': 4,  'close': 2}
RRG2 = {'input': 5, 'output': 1, 'open': 8,  'close': 7}
RRG3 = {'input': 6, 'output': 2, 'open': 11, 'close': 10}
RRG4 = {'input': 9, 'output': 3, 'open': 13, 'close': 12}

rrg = [RRG1, RRG2, RRG3, RRG4]
gas = RRG.RRG(port, rrg)

path = "/tmp/python_unix_sockets_rrg"
server = initialize(path)


def read_device_function(data):

    print data +"data"
    answer = "No data"
    if "Set_" in data:
        device = rrg[int(data.split("_")[1][3]) - 1]
        if len(data.split()) > 1:
            answer = str(gas.write(device, float(data.split()[1])))
    elif "Coil_" in data:
        print data.split("_")
        device = rrg[int(data.split("_")[2][3]) - 1]
        print device
        if data.split("_")[1]=="open":
            answer = gas.gateMode(device, 'open')
        if data.split("_")[1]=="close":
            answer = gas.gateMode(device, 'close')
        if data.split("_")[1]=="regulate":
            answer = gas.gateMode(device)
        if answer:
            answer = "Done"
        else:
            answer = "Nope"
    else:   
        
        device = rrg[int(data[3]) - 1]
        answer = "{:.2f}".format(gas.read(device))
        print gas.read(device)
        
    print answer

    return answer


start(server, read_device_function)
stop(path)
gas.close()