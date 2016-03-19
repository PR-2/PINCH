import threading

from pymodbus.client.sync import ModbusSerialClient


class Connection():
    def __init__(self, indicator_list, coil_on_list, coil_off_list, command_list, port, method="rtu", timeout=1):

        self.indicator_list = indicator_list
        self.coil_on_list = coil_on_list
        self.coil_off_list = coil_off_list
        self.command_list = command_list
        self.lock = threading.Lock()
        self.client = ModbusSerialClient(method=method, port=port, baudrate=19200, stopbits=1, bytesize=8,
                                         timeout=timeout)

    def translate(self, command):
        self.lock.acquire()

# input registers
        if command.split("_")[0] == "IReg":
            rr = self.client.read_input_registers(self.indicator_list[command.split()[0]], 1, unit=0x01)

            self.client.close()
            self.lock.release()
            return rr.getRegister(0)

# coils
        elif command.split("_")[0] == "Coil":
            if command.split()[0] in self.coil_on_list:
                wr = self.client.write_coil(self.coil_on_list[command.split()[0]], 1, unit=0x01)
                rr = self.client.read_coils(self.coil_on_list[command.split()[0]], 1, unit=0x01)
            elif command.split()[0] in self.coil_off_list:
                wr = self.client.write_coil(self.coil_off_list[command.split()[0]], 0, unit=0x01)
                rr = self.client.read_coils(self.coil_off_list[command.split()[0]], 1, unit=0x01)

            self.client.close()
            self.lock.release()
            return rr.getBit(0)

# holding registers
        elif command.split("_")[0] == "HReg":
          #  print command
            if len(command.split()) > 1 and command.split()[1].isdigit():
                wr = self.client.write_registers(self.command_list[command.split()[0]], [int(command.split()[1])], unit=10)
            rr = self.client.read_holding_registers(self.command_list[command.split()[0]], 1, unit=10)
            self.client.close()
            self.lock.release()
            return rr.getRegister(0)

        else:
            return "Not correct command"
            print "Not correct command"
            self.lock.release()