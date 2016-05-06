from pymodbus.client.sync import ModbusTcpClient
from pymodbus.register_write_message import WriteSingleRegisterRequest, WriteSingleRegisterResponse
from pymodbus.register_write_message import ModbusResponse, ModbusRequest
from pymodbus.pdu import ModbusExceptions as merror

import struct

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


class Read_cito_req(ModbusRequest):
    '''
    This function code is used to write a single holding register in a
    remote device.

    The Request PDU specifies the address of the register to
    be written. Registers are addressed starting at zero. Therefore register
    numbered 1 is addressed as 0.
    '''
    function_code = 0x41
    #_rtu_frame_size = 8

    def __init__(self, address=None, value=None, **kwargs):
        ''' Initializes a new instance

        :param address: The address to start writing add
        :param value: The values to write
        '''
        ModbusRequest.__init__(self, **kwargs)
        self.address = address
        self.value = value

    def encode(self):
        ''' Encode a write single register packet packet request

        :returns: The encoded packet
        '''

        if self.skip_encode:
            return self.value
        return struct.pack('>HH', self.address, self.value)
    def decode(self,data):
        if len(data) == 7:
            self.address, func_name, message_len, self.value = struct.unpack('>bbbI', data)
        else:
            self.address, func_name, message_len, self.value = struct.unpack('>bbb' + str(len(data) - 3) + 's',
                                                                             data)

    def execute(self, context):
        ''' Run a write single register request against a datastore

        :param context: The datastore to request from
        :returns: An initialized response, exception message otherwise
        '''
        if not (0 <= self.value <= 0xffff):
            return self.doException(merror.IllegalValue)
        if not context.validate(self.function_code, self.address, 1):
            return self.doException(merror.IllegalAddress)

        context.setValues(self.function_code, self.address, [self.value])
        values = context.getValues(self.function_code, self.address, 1)
        return Read_cito_res(self.address, values[0])

    def __str__(self):
        ''' Returns a string representation of the instance

        :returns: A string representation of the instance
        '''
        return "WriteRegisterRequest %d => %d" % (self.address, self.value)


class Read_cito_res(ModbusResponse):
    '''
    The normal response is an echo of the request, returned after the
    register contents have been written.
    '''
    function_code = 0x41
   # _rtu_frame_size = 8

    def __init__(self, address=None, value=None, **kwargs):
        ''' Initializes a new instance

        :param address: The address to start writing add
        :param value: The values to write
        '''
        ModbusResponse.__init__(self, **kwargs)
        self.address = address
        self.value = value


    def encode(self):
        ''' Encode a write single register packet packet request

        :returns: The encoded packet
        '''
        return struct.pack('>HH', self.address, self.value)

    def decode(self,data):
        if len(data) == 7:
            self.address, func_name, message_len, self.value = struct.unpack('>bbbI', data)
        else:
            self.address, func_name, message_len, self.value = struct.unpack('>bbb' + str(len(data) - 3) + 's',
                                                                             data)

    def __str__(self):
        ''' Returns a string representation of the instance

        :returns: A string representation of the instance
        '''
        params = (self.address, self.value)
        return "WriteRegisterResponse %d => %d" % params




class ReadCitoReq(WriteSingleRegisterRequest):
    function_code = 0x41


    def encode(self):

        ''' Encode a write single register packet packet request

        :returns: The encoded packet
        '''
        if self.skip_encode:
            return self.value
        return struct.pack('>HH', self.address, self.value)

    def decode(self, data):

        ''' Decode a write single register packet packet request

        :param data: The request to decode
        '''
         #struct.unpack('>bbb' + str(len(data) - 3) + 's', '\x0a\x41\x04\x00\x00\x00\x00')
        if len(data) == 7:
            self.address, func_name, message_len, self.value = struct.unpack('>bbbI', data)
        else:
            self.address, func_name, message_len, self.value = struct.unpack('>bbb' + str(len(data) - 3) + 's',
                                                                      data)



    def execute(self, context):
        ''' Run a write single register request against a datastore

        :param context: The datastore to request from
        :returns: An initialized response, exception message otherwise
        '''
        if not (0 <= self.value <= 0xffffffff):
            return self.doException(merror.IllegalValue)
        if not context.validate(self.function_code, self.address, 1):
            return self.doException(merror.IllegalAddress)


        context.setValues(self.function_code, self.address, [self.value])
        values = context.getValues(self.function_code, self.address, 1)
        return ReadCitoRes(self.address, values[0])

class ReadCitoRes(WriteSingleRegisterResponse):
    function_code = 0x41


    def decode(self, data):
        ''' Decode a write single register packet packet request

        :param data: The request to decode
        '''
        # struct.unpack('>bbb' + str(len(data) - 3) + 's', '\x0a\x41\x04\x00\x00\x00\x00')

        if len(data) == 7:
            self.address, func_name, message_len, self.value = struct.unpack('>bbbI', data)
        else:
            self.address, func_name, message_len, self.value = struct.unpack('>bbb' + str(len(data) - 3) + 's',
                                                                             data)


class WriteCitoReq(WriteSingleRegisterRequest):
    function_code = 0x42

    def encode(self):
        ''' Encode a write single register packet packet request

        :returns: The encoded packet
        '''
        if self.skip_encode:
            return self.value
        return struct.pack('>HI', self.address, self.value)

    def decode(self, data):
        ''' Decode a write single register packet packet request

        :param data: The request to decode
        '''
        self.address, self.value = struct.unpack('>HI', data)


    def execute(self, context):
        ''' Run a write single register request against a datastore

        :param context: The datastore to request from
        :returns: An initialized response, exception message otherwise
        '''
        if not (0 <= self.value <= 0xffffffff):
            return self.doException(merror.IllegalValue)
        if not context.validate(self.function_code, self.address, 1):
            return self.doException(merror.IllegalAddress)

        context.setValues(self.function_code, self.address, [self.value])
        values = context.getValues(self.function_code, self.address, 1)
        return WriteCitoRes(self.address, values[0])

class WriteCitoRes(WriteSingleRegisterResponse):
    function_code = 0x42

class ExtendedTcp(ModbusTcpClient):
    def read(self, address, count=1, **kwargs):
        request = Read_cito_req(address, count, **kwargs)
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

#rr = client.write(1001,0, unit=0x0A)
#rr = client.read(8021, [1], unit=0x0A)


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