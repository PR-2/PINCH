import threading

from pymodbus.client.sync import ModbusSerialClient


class Connection_to_capacity_changer():
    def __init__(self):
        self.lock = threading.Lock()

    def translate(self, port, command):
        self.lock.acquire()

        # port ='/dev/ttyUSB0',
        client = ModbusSerialClient(method='rtu', port=port, baudrate=19200, stopbits=1, bytesize=8, timeout=1)

       # print client.connect()
        indicator_list = {"IReg_C-value": 1023,
                          "IReg_C2-value": 1025,
                          "IReg_C1-value": 1027,
                          "IReg_Phase-mismatch": 1033,
                          "IReg_Amplitude-mismatch": 1034,
                          }

        coil_on_list = {"Coil_AutoPhaseSetupOn": 999,
                        "Coil_AutoResistanceSetupOn": 1000,
                        "Coil_EEPROM-writeOn": 10001,
                        "Coil_EngineOn": 1002,
                        "Coil_AutoReturnOn": 1003}

        coil_off_list = {"Coil_AutoPhaseSetupOff": 999,
                        "Coil_AutoResistanceSetupOff": 1000,
                        "Coil_EEPROM-writeOff": 10001,
                        "Coil_EngineOff": 1002,
                        "Coil_AutoReturnOff": 1003}

        command_list = {"HReg_InstallationPhaseSensorZero": 1002,
                        "HReg_InstallationAmplitudeSensorZero": 1003,
                        "HReg_PhaseTuningSensitivity": 1005,
                        "HReg_ResistanceTuningSensitivity": 1006,
                        "HReg_Min-C2-capacity": 1007,
                        "HReg_Max-C2-capacity": 1008,
                        "HReg_Min-C1-capacity": 1009,
                        "HReg_Max-C1-capacity": 1010,
                        "HReg_Set-C-value": 1011,
                        "HReg_Set-C2-value": 1012,
                        "HReg_Modbus-address": 1013,
                        "HReg_Threshold-auto-negotiation": 1014,
                        "HReg_C-max-limit": 1015,
                        "HReg_C-min-limit": 1016,
                        "HReg_C2-max-limit": 1017,
                        "HReg_C2-min-limit": 1018}

        # input registers
        # print command.split()
        if command.split("_")[0] == "IReg":

            rr = client.read_input_registers(indicator_list[command.split()[0]], 1, unit=10)

            client.close()
            self.lock.release()

            return rr.getRegister(0)
            # coils
        elif command.split("_")[0] == "Coil":
            if command.split()[0] in coil_on_list:
                wr = client.write_coil(coil_on_list[command.split()[0]], 1, unit=10)
                rr = client.read_coils(coil_on_list[command.split()[0]], 1, unit=10)
            elif command.split()[0] in coil_off_list:
                wr = client.write_coil(coil_off_list[command.split()[0]], 0, unit=10)
                rr = client.read_coils(coil_off_list[command.split()[0]], 1, unit=10)

            client.close()
            self.lock.release()
            return rr.getBit(0)

        elif command.split("_")[0] == "HReg":
            print command
            if len(command.split()) > 1 and command.split()[1].isdigit():
                print command.split()[1]
                print int(command.split()[1])

                wr = client.write_registers(command_list[command.split()[0]], [int(command.split()[1])], unit=10)
                print "Done"
            rr = client.read_holding_registers(command_list[command.split()[0]], 1, unit=10)
            client.close()
            self.lock.release()
            return rr.getRegister(0)

        else:
            return "Not correct command"
            print "Not correct command"
            self.lock.release()
