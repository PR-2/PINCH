import serial
import time

class Arduino_DAADC():
    def __init__(self, serialPort, baud=9600):
        self.errorCode = 0
        self.time2wait = 0.1
        try:
            self.connection = serial.Serial(serialPort, baudrate=baud,timeout=1)
        except serial.serialutil.SerialException as se:
            raise RRG_ArduinoError(se)
        if  self.connection.isOpen():
            self.connection.close()
        self.connection.open()
        time.sleep(2)

    def DO(self, pinNO, mode = 0, unitID = 1):
        message  = str(unitID).zfill(3)
        message += 'DO'
        message += str(pinNO).zfill(2)
        message += str(mode)
        message += str(self.checksum(message)).zfill(3) + '\n'
        self.connection.write(message.encode())
        time.sleep(self.time2wait)
        message = self.connection.readline()
        if self.checkMes(message, unitID) and (message[3:-4] == 'SETTED'):
            return True
        self.errorCode = 'Error code ' + str(message[-6:-4])
        return False

    def DI(self, pinNO, unitID = 1):
        message  = str(unitID).zfill(3)
        message += 'DI'
        message += str(pinNO).zfill(2)
        message += str(self.checksum(message)).zfill(3) + '\n'
        self.connection.write(message.encode())
        time.sleep(self.time2wait)
        message = self.connection.readline()
        if self.checkMes(message, unitID):
            return int(message[7])
        self.errorCode = 'Error code ' + str(message[-6:-4])
        return False

    def AO(self, pinNO, value, unitID = 1):
        message  = str(unitID).zfill(3)
        message += 'AO'
        message += str(pinNO).zfill(2)
        message += str(int(255*value/5)).zfill(4)
        message += str(self.checksum(message)).zfill(3) + '\n'
        self.connection.write(message.encode())
        time.sleep(self.time2wait)
        message = self.connection.readline()
        if self.checkMes(message, unitID) and (message[3:-4] == 'SETTED'):
            return True
        self.errorCode = 'Error code ' + str(message[-6:-4])
        return False

    def AI(self, pinNO, unitID = 1):
        message  = str(unitID).zfill(3)
        message += 'AI'
        message += str(pinNO).zfill(2)
        message += str(self.checksum(message)).zfill(3) + '\n'
        self.connection.write(message.encode())
        time.sleep(self.time2wait)
        message = self.connection.readline()
        if self.checkMes(message, unitID):
            return (5.0*int(message[7:-4])/1023.0)
        self.errorCode = 'Error code ' + str(message[-6:-4])
        return False

    def checksum(self, string):
        result = 0
        for ch in string:
            result += ord(ch)
        return (result % 256)

    def checkMes(self, message, unitID):
        _unitID = int(message[:3])
        _chsum  = int(message[-4:-1])
        chsum   = self.checksum(message[:-4])
        if (unitID == _unitID) and (chsum == _chsum):
            return True
        return False

    def close(self):
        try:
            self.connection.close()
        except serial.serialutil.SerialException as se:
            raise RRG_ArduinoError(se)

class ArduinoError(Exception):
    pass
