import struct


class DataTypeError(Exception):
    pass


class DataType(object):
    '''
    The base class for the three different data types found
    in a Starcraft/Broodwar replay file.  Subclasses should
    define their own class attribute `symbol` which represents
    the character to use in `struct.unpack()`.
    '''
    symbol = 'x'

    def __init__(self, size):
        '''
        The constructor accepts either an integer or another DataType
        instance.  If a DataType instance is given, the result of reading
        that DataType will be used as the size.
        '''
        if isinstance(size, int):
            self.size = size
        elif isinstance(size, DataType):
            self.size = None
        else:
            raise DataTypeError('"size" must be either an integer or '
                                'an instance of DataType')

    def __str__(self):
        return '<%s: %r>' % (self.__class__.__name__,
                             self.get_unpack_format())

    def __repr__(self):
        return str(self)

    def get_unpack_format(self):
        '''
        Return the struct.unpack formatted string.
        '''
        return '%d%s' % (self.size, self.symbol)


class Byte(DataType):
    symbol = 'B'


class Word(DataType):
    symbol = 'H'


class DWord(DataType):
    symbol = 'I'


class AssocList(object):
    def __init__(self, alist):
        self.alist = alist

    def __getitem__(self, key):
        for k, v in self.alist:
            if k == key:
                return v
        raise KeyError('No such key: %s' % key)

    def __setitem__(self, key, value):
        for (i, (k, v)) in enumerate(self.alist):
            if k == key:
                self.alist[i] = (key, value)
                return
        self.alist.append((key, value))

    def __str__(self):
        return str(self.alist)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        for t in self.alist:
            yield t
