import RRG, sys, time

RRG1 = {'input': 3, 'output': 0, 'open': 4,  'close': 2}
RRG2 = {'input': 5, 'output': 1, 'open': 8,  'close': 7}
RRG3 = {'input': 6, 'output': 2, 'open': 11, 'close': 10}
RRG4 = {'input': 9, 'output': 3, 'open': 13, 'close': 12}

RRGs = [RRG1, RRG2, RRG3, RRG4]

gas = RRG.RRG(sys.argv[1], RRGs)

for rrg in RRGs:
    print(gas.gateMode(rrg, 'open'))
    time.sleep(5)
    print(gas.gateMode(rrg, 'close'))
    time.sleep(5)
    print(gas.gateMode(rrg))
    time.sleep(5)
    print gas.read(rrg)

gas.closeConnection()
