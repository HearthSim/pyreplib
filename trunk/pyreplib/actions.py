import struct

from pyreplib.datatypes import Byte, Word, DWord, AssocList


class Field(object):
    '''
    `creation_counter` is used so that we can keep track of which fields
    were created first in the different Actions.
    '''

    creation_counter = 0

    def __init__(self, cls, size):
        self.cls = cls
        self.size = size
        self.data = None
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def _get_size(self):
        if isinstance(self.size, int):
            return self.size
        elif isinstance(self.size, Field):
            return self.size.data
        else:
            raise TypeError('"size" must be an int or a Field')

    def read(self, buf):
        datatype = self.cls(self._get_size())
        length = struct.calcsize(datatype.get_unpack_format())
        s = buf.read(length)
        if len(s) != length:
            raise ReadError('Could not read %d bytes, only %d available'
                            % (length, len(s)))
        t = struct.unpack(datatype.get_unpack_format(), s)
        if len(t) == 1:
            self.data = t[0]
        else:
            self.data = t
        return self.data


class ActionBase(type):
    '''
    Meta-class for all Action objects.  This will set a `fields`
    attribute containing an AssocList of the binary fields to
    read, ordered by their creation_count (as specified in
    datatypes.DataType.)
    '''
    def __new__(cls, name, base, attrs):
        fields = list(ActionBase.get_declared_fields(attrs))
        fields.sort(cmp=lambda a,b: cmp(a[1].creation_counter,
                                        b[1].creation_counter))
        attrs['fields'] = AssocList(fields)
        return super(ActionBase, cls).__new__(cls, name, base, attrs)

    def get_declared_fields(attrs):
        for attr in attrs.iteritems():
            if isinstance(attr[1], Field):
                yield attr
    get_declared_fields = staticmethod(get_declared_fields)


class Action(object):
    '''
    Base class for all Action objects.  All subclasses should define
    an `id` attribute and the different data fields of that particular
    action.  The `name` attribute can optionally be set if the name
    of the action differs from the name of the class (useful if you
    wish to use spaces.)
    '''
    __metaclass__ = ActionBase

    def __init__(self, tick, player):
        self.tick = tick
        self.player = player


class Select(Action):
    id = 0x09
    count = Field(Byte, 1)
    unit_ids = Field(Word, count)

# Accumulate all the Action subclasses in a dictionary and use their
# `id` attribute to index them.
action_classes = dict((cls.id, cls) for cls in Action.__subclasses__())
