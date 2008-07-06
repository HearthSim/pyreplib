import struct

Byte = 'B'
Word = 'H'
DWord = 'I'

class AssocList(list):
    def __getitem__(self, key):
        for k, v in self:
            if k == key:
                return v
        raise KeyError('No such key: %s' % key)

    def __setitem__(self, key, value):
        for (i, (k, v)) in enumerate(self):
            if k == key:
                super(AssocList, self).__setitem__(i, (key, value))
                return
        self.append((key, value))

