import Arduino_DAADC as ard

class RRG():
    def __init__(self, serialPort, RRGs, unitID = 1):
        self.unitID = unitID
        self.RRGs = RRGs
        self.Arduino = ard.Arduino_DAADC(serialPort)
        for rrg in self.RRGs:
            self.write(rrg, 0)
            self.gateMode(rrg)


    def readAll(self):
        return [self.read(rrg) for rrg in self.RRGs]

    def read(self, rrg):
        return 100*self.Arduino.AI(rrg['output'], self.unitID)/10.

    def write(self, rrg, gasFlow):
        return self.Arduino.AO(rrg['input'], (5*gasFlow/100.), self.unitID)

    def gateMode(self, rrg, mode = 'regulation'):
        if   (mode == 'open'):
            self.Arduino.DO(rrg['open'], 1)
            self.Arduino.DO(rrg['close'], 1)
            return self.Arduino.DO(rrg['open'], 0)
        elif (mode == 'close'):
            self.Arduino.DO(rrg['open'], 1)
            self.Arduino.DO(rrg['close'], 1)
            return self.Arduino.DO(rrg['close'], 0)
        elif (self.Arduino.DO(rrg['open'], 1) == True and self.Arduino.DO(rrg['close'], 1) == True):
            return True
        return False

    def closeConnection(self):
        self.Arduino.close()


class RRGError(Exception):
    pass
