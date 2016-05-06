import Arduino_DAADC as ard

class RRG():
    def __init__(self, serialPort, RRGs, unitID = 1):
        self.unitID = unitID
        self.RRGs = RRGs
        self.Arduino = ard.Arduino_DAADC(serialPort)
#        for rrg in self.RRGs:
#            self.write(rrg, 0)


    def readAll(self):
        gasFlows = []
        for rrg in self.RRGs:
            gasFlows.append(100*self.Arduino.AI(rrg['output'], self.unitID)/10.)
        return gasFlows

    def read(self, rrg):
        return 100*self.Arduino.AI(rrg['output'], self.unitID)/10.

    def write(self, rrg, gasFlow):
        return self.Arduino.AO(rrg['input'], (5*gasFlow/100.), self.unitID)

    def gateMode(self, mode):
        return 0

    def close(self):
        self.Arduino.close()


class RRGError(Exception):
    pass
