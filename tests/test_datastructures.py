import unittest

from pyreplib.datastructures import Byte, Word, DWord, AssocList

class TestDataTypes(unittest.TestCase):
    def test_byte(self):
        self.assertEquals(Byte, 'B')
        self.assertEquals(Word, 'H')
        self.assertEquals(DWord, 'I')


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
        self.assertEquals(len(self.alist), 3)
        self.assertEquals(self.alist, [('a', 'alpha'),
                                       ('b', 'beta'),
                                       ('c', 'charlie')])

        self.alist['d'] = 'delta'
        self.assertEquals(len(self.alist), 4)
        self.assertEquals(self.alist['d'], 'delta')
        self.assertEquals(self.alist, [('a', 'alpha'),
                                       ('b', 'beta'),
                                       ('c', 'charlie'),
                                       ('d', 'delta')])




if __name__ == '__main__':
    unittest.main()
