import unittest

from pyreplib.datastructures import Byte, Word, DWord, DataTypeError, AssocList

class TestDataType(unittest.TestCase):
    def test_byte(self):
        self.assertEquals(Byte.symbol, 'B')
        byte = Byte(1)
        self.assertEquals(byte.size, 1)
        self.assertEquals(byte.get_unpack_format(), '1B')
        byte.size = 12
        self.assertEquals(byte.size, 12)
        self.assertEquals(byte.get_unpack_format(), '12B')

    def test_word(self):
        self.assertEquals(Word.symbol, 'H')
        word = Word(1)
        self.assertEquals(word.size, 1)
        self.assertEquals(word.get_unpack_format(), '1H')
        word.size = 12
        self.assertEquals(word.size, 12)
        self.assertEquals(word.get_unpack_format(), '12H')

    def test_dword(self):
        self.assertEquals(DWord.symbol, 'I')
        dword = DWord(1)
        self.assertEquals(dword.size, 1)
        self.assertEquals(dword.get_unpack_format(), '1I')
        dword.size = 12
        self.assertEquals(dword.size, 12)
        self.assertEquals(dword.get_unpack_format(), '12I')

    def test_constructor(self):
        byte = Byte(1)
        self.assert_(Byte(10), 'Constructing from an int')
        self.assert_(Byte(byte), 'Constructing from a DataType')
        self.assertRaises(DataTypeError, lambda: Byte('hello'))


class TestAssocList(unittest.TestCase):
    def setUp(self):
        self.alist = AssocList([('a', 'alpha'),
                                ('b', 'bravo'),
                                ('c', 'charlie')])

    def test_getitem(self):
        self.assertEquals(self.alist['a'], 'alpha')
        self.assertEquals(self.alist['b'], 'bravo')
        self.assertEquals(self.alist['c'], 'charlie')
        self.assertRaises(KeyError, lambda: self.alist['d'])

    def test_setitem(self):
        self.alist['b'] = 'beta'
        self.assertEquals(self.alist['b'], 'beta')
        self.assertEquals(self.alist.alist, [('a', 'alpha'),
                                             ('b', 'beta'),
                                             ('c', 'charlie')])
        self.alist['d'] = 'delta'
        self.assertEquals(self.alist['d'], 'delta')
        self.assertEquals(self.alist.alist[3], ('d', 'delta'))



if __name__ == '__main__':
    unittest.main()
