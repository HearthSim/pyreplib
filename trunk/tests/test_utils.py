import unittest

from pyreplib import utils
from pyreplib import actions
from pyreplib.replay import Player


class TestAverage(unittest.TestCase):
    def test_avg(self):
        self.assertEquals(utils.avg([]), None)
        self.assertAlmostEquals(utils.avg([1]), 1)
        self.assertAlmostEquals(utils.avg([2, 4]), 3)
        self.assertAlmostEquals(utils.avg([1, 2]), 1.5)


class TestAPM(unittest.TestCase):
    def setUp(self):
        self.player = Player('', '', '', '', '')
        self.player.actions = [
            actions.Action(1),
            actions.Action(2),
            actions.Action(3),
            actions.Action(24 * 60 + 1),
            actions.Action(24 * 60 + 2),
            actions.Action(24 * 60 * 2 + 1),
        ]

    def test_actions_per_minute(self):
        self.assertEquals(list(utils.actions_per_minute(self.player)),
                          [3, 2, 1])

    def test_apm_stats(self):
        self.assertEquals(utils.apm_stats(self.player), (1, 2.0, 3))


class TestDistribution(unittest.TestCase):
    def setUp(self):
        self.player = Player('', '', '', '', '')

    def test_building_distribution_build(self):
        for building_id in (0x6D, 0x6D, 0x6F, 0x6B):
            instance = actions.Build(0)
            instance.building_type_id = building_id
            self.player.actions.append(instance)
        distribution = utils.building_distribution(self.player)
        self.assertEquals(len(distribution), 3)
        self.assertEquals(distribution['Supply Depot'], 2)
        self.assertEquals(distribution['Barracks'], 1)
        self.assertEquals(distribution['ComSat'], 1)

    def test_building_distribution_morph(self):
        for building_id in (0x83, 0x83, 0x95, 0x8E):
            instance = actions.Morph(0)
            instance.building_type_id = building_id
            self.player.actions.append(instance)
        distribution = utils.building_distribution(self.player)
        self.assertEquals(len(distribution), 3)
        self.assertEquals(distribution['Hatchery'], 2)
        self.assertEquals(distribution['Extractor'], 1)
        self.assertEquals(distribution['Spawning Pool'], 1)

    def test_unit_distribution_train(self):
        for unit_id in (0x00, 0x00, 0x00, 0x07, 0x07, 0x02, 0x05, 0x02):
            instance = actions.Train(0)
            instance.unit_type_id = unit_id
            self.player.actions.append(instance)
        distribution = utils.unit_distribution(self.player)
        self.assertEquals(len(distribution), 4)
        self.assertEquals(distribution['Marine'], 3)
        self.assertEquals(distribution['SCV'], 2)
        self.assertEquals(distribution['Vulture'], 2)
        self.assertEquals(distribution['Siege Tank'], 1)

    def test_unit_distribution_hatch(self):
        for unit_id in (0x25, 0x25, 0x25, 0x29, 0x29, 0x26, 0x27, 0x26):
            instance = actions.Hatch(0)
            instance.unit_type_id = unit_id
            self.player.actions.append(instance)
        distribution = utils.unit_distribution(self.player)
        self.assertEquals(len(distribution), 4)
        self.assertEquals(distribution['Zergling'], 3)
        self.assertEquals(distribution['Drone'], 2)
        self.assertEquals(distribution['Hydralisk'], 2)
        self.assertEquals(distribution['Ultralisk'], 1)
