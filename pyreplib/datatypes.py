import struct

class DataType(object):
    symbol = 'x'

    def __init__(self, n):
        self.n = n

    def get_unpack_string(self):
        return '%d%s' % (self.n, self.symbol)

class Byte(DataType):
    symbol = 'B'

class Word(DataType):
    symbol = 'H'

class DWord(DataType):
    symbol = 'I'
