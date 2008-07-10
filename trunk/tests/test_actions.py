import struct
import unittest
from cStringIO import StringIO
try:
    from IPython.Shell import IPShellEmbed
except ImportError:
    pass

from pyreplib.actions import *


class TestActionBase(unittest.TestCase):
    def setUp(self):
        class TestAction(object):
            __metaclass__ = ActionBase
            field1 = Field(Byte, 1)
            field2 = Field(Word, 2)
            field3 = Field(DWord, field1)
            non_field = 10

        self.action_cls = TestAction

    def test_class(self):
        self.assertEquals(self.action_cls.name, 'TestAction')

        # Check that `base_fields` only contains Field instances.
        self.assertEquals(len(self.action_cls.base_fields), 3)
        self.assert_('field1' in self.action_cls.base_fields)
        self.assert_('field2' in self.action_cls.base_fields)
        self.assert_('field3' in self.action_cls.base_fields)

        # Ensure that the fields will be in order when read
        self.assert_(self.action_cls.field1 <
                     self.action_cls.field2 <
                     self.action_cls.field3)

        # Check Fields' attributes
        self.assertEquals(self.action_cls.field1.datatype, Byte)
        self.assertEquals(self.action_cls.field1.size, 1)
        self.assertEquals(self.action_cls.field1.length, 1)
        self.assertEquals(self.action_cls.field1.format, '<1B')

        self.assertEquals(self.action_cls.field2.datatype, Word)
        self.assertEquals(self.action_cls.field2.size, 2)
        self.assertEquals(self.action_cls.field2.length, 4)
        self.assertEquals(self.action_cls.field2.format, '<2H')

        self.assertEquals(self.action_cls.field3.datatype, DWord)
        self.assertEquals(self.action_cls.field3.size, self.action_cls.field1)
        self.assert_(not hasattr(self.action_cls.field3, 'length'))
        self.assert_(not hasattr(self.action_cls.field3, 'format'))



class TestSelect(unittest.TestCase):
    def test_read(self):
        valid_one_unit = StringIO(struct.pack('< B H', 1, 1))
        valid_two_units = StringIO(struct.pack('< B H H', 2, 1, 2))

        instance = Select(0)
        n = instance.read(valid_one_unit)
        self.assertEquals(n, 3)
        self.assertEquals(instance.count, 1)
        self.assertEquals(instance.unit_ids, (1,))

        n = instance.read(valid_two_units)
        self.assertEquals(n, 5)
        self.assertEquals(instance.count, 2)
        self.assertEquals(instance.unit_ids, (1, 2))


class TestShiftSelect(unittest.TestCase):
    def test_read(self):
        valid_one_unit = StringIO(struct.pack('< B H', 1, 1))
        valid_two_units = StringIO(struct.pack('< B H H', 2, 1, 2))

        instance = ShiftSelect(0)
        n = instance.read(valid_one_unit)
        self.assertEquals(n, 3)
        self.assertEquals(instance.count, 1)
        self.assertEquals(instance.unit_ids, (1,))

        n = instance.read(valid_two_units)
        self.assertEquals(n, 5)
        self.assertEquals(instance.count, 2)
        self.assertEquals(instance.unit_ids, (1, 2))


class TestShiftDeselect(unittest.TestCase):
    def test_read(self):
        valid_one_unit = StringIO(struct.pack('< B H', 1, 1))
        valid_two_units = StringIO(struct.pack('< B H H', 2, 1, 2))

        instance = ShiftDeselect(0)
        n = instance.read(valid_one_unit)
        self.assertEquals(n, 3)
        self.assertEquals(instance.count, 1)
        self.assertEquals(instance.unit_ids, (1,))

        n = instance.read(valid_two_units)
        self.assertEquals(n, 5)
        self.assertEquals(instance.count, 2)
        self.assertEquals(instance.unit_ids, (1, 2))


class TestBuild(unittest.TestCase):
    def test_read(self):
        valid = StringIO(struct.pack('< B H H H', 0x6A, 0, 0, 1))
        instance = Build(0)
        n = instance.read(valid)
        self.assertEquals(n, 7)
        self.assertEquals(instance.building_type_id, 0x6A)
        self.assertEquals(instance.pos_x, 0)
        self.assertEquals(instance.pos_y, 0)
        self.assertEquals(instance.building_id, 1)

    def test_get_building_type(self):
        instance = Build(0)
        instance.building_type_id = 0x6A
        self.assertEquals(instance.get_building_type(), 'Command Center')
        instance.building_type_id = 0xFF
        self.assertEquals(instance.get_building_type(), '0xff')


class TestVision(unittest.TestCase):
    def test_read(self):
        valid = StringIO(struct.pack('<2B', 0, 1))
        instance = Vision(0)
        n = instance.read(valid)
        self.assertEquals(n, 2)
        self.assertEquals(instance.unknown, (0, 1))


class TestAlly(unittest.TestCase):
    def test_read(self):
        valid = StringIO(struct.pack('<4B', 0, 1, 2, 3))
        instance = Ally(0)
        n = instance.read(valid)
        self.assertEquals(n, 4)
        self.assertEquals(instance.unknown, (0, 1, 2, 3))


class TestHotkey(unittest.TestCase):
    def test_read(self):
        valid_set = StringIO(struct.pack('< B B', 0, 1))
        valid_get = StringIO(struct.pack('< B B', 1, 1))
        instance = Hotkey(0)

        n = instance.read(valid_set)
        self.assertEquals(n, 2)
        self.assertEquals(instance.set_or_get, 0)
        self.assertEquals(instance.group, 1)

        n = instance.read(valid_get)
        self.assertEquals(n, 2)
        self.assertEquals(instance.set_or_get, 1)
        self.assertEquals(instance.group, 1)


class TestMove(unittest.TestCase):
    def test_read(self):
        absolute_move = StringIO(struct.pack('< H H H H B', 100, 100, 0xFFFF, 0, 0))
        follow_move = StringIO(struct.pack('< H H H H B', 200, 200, 1, 0, 0))
        instance = Move(0)

        n = instance.read(absolute_move)
        self.assertEquals(n, 9)
        self.assertEquals(instance.pos_x, 100)
        self.assertEquals(instance.pos_y, 100)
        self.assertEquals(instance.unit_id, 0xFFFF)
        self.assertEquals(instance.unknown1, 0)
        self.assertEquals(instance.unknown2, 0)

        n = instance.read(follow_move)
        self.assertEquals(n, 9)
        self.assertEquals(instance.pos_x, 200)
        self.assertEquals(instance.pos_y, 200)
        self.assertEquals(instance.unit_id, 1)
        self.assertEquals(instance.unknown1, 0)
        self.assertEquals(instance.unknown2, 0)


class TestAttack(unittest.TestCase):
    def test_get_type(self):
        instance = Attack(0)
        instance.type_id = 0
        self.assertEquals(instance.get_type(), 'Move with right click')
        instance.type_id = 0xFF
        self.assertEquals(instance.get_type(), '0xff')
