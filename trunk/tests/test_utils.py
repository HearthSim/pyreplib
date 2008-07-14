import unittest

from pyreplib import utils
from pyreplib.replay import Player
from pyreplib.actions import Action


class TestAverage(unittest.TestCase):
    def test_avg(self):
        self.assertEquals(utils.avg([]), None)
        self.assertAlmostEquals(utils.avg([1]), 1)
        self.assertAlmostEquals(utils.avg([2, 4]), 3)
        self.assertAlmostEquals(utils.avg([1, 2]), 1.5)


class TestAPM(unittest.TestCase):
    def setUp(self):
        self.player = Player(*['']*5)
        self.player.actions = [
            Action(1),
            Action(2),
            Action(3),
            Action(24 * 60 + 1),
            Action(24 * 60 + 2),
            Action(24 * 60 * 2 + 1),
        ]

    def test_actions_per_minute(self):
        self.assertEquals(list(utils.actions_per_minute(self.player)),
                          [3, 2, 1])

    def test_apm_stats(self):
        self.assertEquals(utils.apm_stats(self.player), (1, 2.0, 3))
