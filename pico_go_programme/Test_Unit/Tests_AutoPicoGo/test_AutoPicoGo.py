from AutoFeatures.AutoPicoGo import AutoPicoGo
from Test_Unit.shared import StubsAndMocks
import unittest

def autoFactory():
    auto = AutoPicoGo()
    return auto

class TestAutoPicoGo(unittest.TestCase):
    def setUp(self):
        self.ObstacleDetection = StubsAndMocks.MockObstacleDetection()
        self.LineDetection = StubsAndMocks.MockLineDetection()
        self.instance = autoFactory()

    def test_follow_line_follows_line(self):

    def test_follow_line_sees_obstacle(self):

    def test_drive_around_obstacle_leaving_line_to_avoid_obstacle(self):

    def test_drive_around_obstacle_for_multiple_cycles(self):

    def test_
    
    def test_act

    def test_act
