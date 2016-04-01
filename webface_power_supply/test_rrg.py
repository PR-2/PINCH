import RRG, sys

RRG1 = {'input': 3, 'output': 0}
RRG2 = {'input': 5, 'output': 1}
RRG3 = {'input': 6, 'output': 2}
RRG4 = {'input': 9, 'output': 3}



gas = RRG.RRG(sys.argv[1], [RRG1, RRG2, RRG3, RRG4])
for i in range(30):
    print gas.read(RRG1)


gas.close()
