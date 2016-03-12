import threading

from pymodbus.client.sync import ModbusSerialClient


class Connection_to_power_supply():
    def __init__(self):
        self.lock = threading.Lock()

    def translate(self, port, command):
        self.lock.acquire()

        # port ='/dev/ttyUSB0',
        client = ModbusSerialClient(method='rtu', port=port, baudrate=19200, stopbits=1, bytesize=8, timeout=0.3)

       # print client.connect()
        indicator_list = {"IReg_State": 0,
                          "IReg_Voltage": 2,
                          "IReg_Current": 3,
                          "IReg_Power": 4,
                          "IReg_Sec": 5,
                          "IReg_Min": 6,
                          "IReg_Hour": 7}

        coil_on_list = {"Coil_ON": 1,
                        "Coil_StTimerON": 2,
                        "Coil_RstTimer": 3,
                        "Coil_IgnOn": 4,
                        "Coil_OutSwitch_B": 5}

        coil_off_list = {"Coil_OFF": 1,
                         "Coil_StTimerOFF": 2,
                         "Coil_IgnOff": 4,
                         "Coil_OutSwitch_A": 5}

        command_list = {"HReg_StabMode": 16,
                        "HReg_Voltage": 17,
                        "HReg_Current": 18,
                        "HReg_Power": 19,
                        "HReg_Mode": 20,
                        "HReg_Freq": 21,
                        "HReg_DCyo": 22,
                        "HReg_Sec": 23,
                        "Send_HReg_Min": 24,
                        "HReg_Hour": 25,
                        "HReg_RemCtrl": 26,
                        "HReg_ArcCnt": 27,}

        # input registers
        # print command.split()
        if command.split("_")[0] == "IReg":
            rr = client.read_input_registers(indicator_list[command.split()[0]], 1, unit=0x01)

            client.close()
            self.lock.release()
            return rr.getRegister(0)
            # coils
        elif command.split("_")[0] == "Coil":
            if command.split()[0] in coil_on_list:
                wr = client.write_coil(coil_on_list[command.split()[0]], 1, unit=0x01)
                rr = client.read_coils(coil_on_list[command.split()[0]], 1, unit=0x01)
            elif command.split()[0] in coil_off_list:
                wr = client.write_coil(coil_off_list[command.split()[0]], 0, unit=0x01)
                rr = client.read_coils(coil_off_list[command.split()[0]], 1, unit=0x01)

            client.close()
            self.lock.release()
            return rr.getBit(0)

        elif len(command.split()) > 1 and command.split("_")[0] == "HReg":

            if command.split()[1].isdigit():
                wr = client.write_registers(command_list[command.split()[0]], [int(command.split()[1])], unit=0x01)
                rr = client.read_holding_registers(command_list[command.split()[0]], 1, unit=0x01)
                client.close()
                self.lock.release()
                return rr.getRegister(0)

        else:
            return "Not correct command"
            print "Not correct command"
            self.lock.release()
