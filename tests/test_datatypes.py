import unittest

import datatypes

class TestDataTypes(unittest.TestCase):
    def test_byte(self):
        byte = datatypes.Byte(1)
        self.assertEquals(byte.n, 1)
        self.assertEquals(byte.unpack_string, '1B')
        byte.n = 12
        self.assertEquals(byte.n, 12)
        self.assertEquals(byte.unpack_string, '12B')

    def test_word(self):
        word = datatypes.Word(1)
        self.assertEquals(word.n, 1)
        self.assertEquals(word.unpack_string, '1H')
        word.n = 12
        self.assertEquals(word.n, 12)
        self.assertEquals(word.unpack_string, '12H')

    def test_dword(self):
        dword = datatypes.DWord(1)
        self.assertEquals(dword.n, 1)
        self.assertEquals(dword.unpack_string, '1I')
        dword.n = 12
        self.assertEquals(dword.n, 12)
        self.assertEquals(dword.unpack_string, '12I')

if __name__ == '__main__':
    unittest.main()
