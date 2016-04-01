import Arduino_DAADC as ard

class RRG():
    def __init__(self, serialPort, RRGs, unitID = 1):
        self.unitID = unitID
        self.RRGs = RRGs
        self.Arduino = ard.Arduino_DAADC(serialPort)

    def readAll(self):
        gasFlows = []
        for rrg in self.RRGs:
            gasFlows.append(50*self.Arduino.AI(rrg['output'], self.unitID)/5)
        return gasFlows

    def read(self, rrg):
        return 50*self.Arduino.AI(rrg['output'], self.unitID)/5

    def write(self, rrg, gasFlow):
        return self.Arduino.AO(rrg['input'], (5*gasFlow/50), self.unitID)

    def gateMode(self, mode):
        return 0

    def close(self):
        self.Arduino.close()


class RRGError(Exception):
    pass
