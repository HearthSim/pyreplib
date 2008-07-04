import struct

from pyreplib.datatypes import Byte, Word, DWord

class ReadError(IOError):
    pass

class ActionUnpacker(object):
    def __init__(self, buf):
        self.buf = buf

    def read(self, size):
        return self.buf.read(size)

    def unpack(self, format):
        s = self.read(struct.calcsize(format))
        t = struct.unpack(format, s)
        if len(t) == 1:
            return t[0]
        else:
            return t

    def parse(self):
        try:
            tick, player_id = self.unpack('IB')
            action_id = self.unpack('B')
            yield action_id
        except ReadError:
            pass

class Selection(Action):
    count = Byte(1)
    units = Word(count)
