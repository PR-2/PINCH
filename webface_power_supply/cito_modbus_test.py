from pymodbus.client.sync import ModbusTcpClient
from pymodbus.register_write_message import ReadCitoReq,ReadCitoRes, WriteCitoReq, WriteCitoRes

from pymodbus.pdu import ModbusExceptions as merror

import struct

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)



class ExtendedTcp(ModbusTcpClient):
    def read(self, address, count=1, **kwargs):
        request = ReadCitoReq(address, count, **kwargs)
        print request
        return self.execute(request)

    def write(self, address, count=1, **kwargs):
        request = WriteCitoReq(address, count, **kwargs)
        print request
        return self.execute(request)

client = ExtendedTcp("10.0.20.8")
#client = ExtendedTcp("127.0.0.1")
print client.connect()
#rr = client.write_register(0xA,1,unit=0x0A)
rr = client.read(10, 1, unit=0x0A)
print "response = " + rr.value
rr = client.read(11, 1, unit=0x0A)
print "response = " + rr.value
rr = client.read(12, 1, unit=0x0A)
print "response = " + rr.value



rr = client.read(8000, 1, unit=0x0A)
print "response = " + rr.value
rr = client.read(8011, 1, unit=0x0A)
print "response = " + rr.value
rr = client.read(8021, 1, unit=0x0A)
print "response = " + rr.value
rr = client.read(8022, 1, unit=0x0A)
print "response = " + rr.value
rr = client.read(8023, 1, unit=0x0A)
print "response = " + rr.value


#rr = client.write(1001,0, unit=0x0A)
rr = client.write(1206, 0, unit=0x0A)
#rr = client.read(8021, [1], unit=0x0A)
print rr


#
# 0a 41 00 0a 00 01

#  Header
#  Address 0x0A
#  Function code 0x41
#  Command number 0x00 0x0A
#  Data 0x00
#  CRC16
# Header:
# (2 bytes)
# (1 byte)
# (1 byte) (2 bytes)
# (1 to 249 bytes) (2 bytes)