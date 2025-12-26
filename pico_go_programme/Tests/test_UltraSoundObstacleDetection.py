from Tests import test_helpers
from AutoFeatures import UltraSoundObstacleDetection

import unittest


class TestUltraSoundObstacleDetection(unittest.TestCase):
    def setUp(self):
        self.time = test_helpers.TimeServiceStub(0)
        self.sensor = test_helpers.SensorStub(100)
        # use short times so tests run fast
        self.instance = UltraSoundObstacleDetection.UltraSoundObstacleDetection(
            UltraSoundSensor=self.sensor,
            TimeService=self.time,
            obstacle_forget_time=3000,
            obstacle_recognition_time=50, 
            obstacle_remember_time=2000,
            obstacle_recognition_distance=20)
        
        
    def test_is_obstacle_in_sight(self):
        self.sensor.set_distance(5)
        self.instance.detect_obstacle()
        self.assertTrue(self.instance.is_seeing_obstacle)

    def test_is_obstacle_not_in_sight(self):
        self.sensor.set_distance(100)
        self.instance.detect_obstacle()
        self.assertFalse(self.instance.is_seeing_obstacle)

    def test_is_remembering_obstacle(self):
        self.sensor.set_distance(5)
        self.instance.detect_obstacle()

        self.time.advance(2000)

        self.instance.detect_obstacle()

        self.assertTrue(self.instance.is_remembering_obstacle)

    def test_will_forget_obstacle(self):
        self.instance.is_remembering_obstacle = True
        self.assertTrue(self.instance.is_remembering_obstacle)
        
        self.sensor.set_distance(4000)
        self.instance.detect_obstacle()
        self.assertFalse(self.instance.is_seeing_obstacle)
                                  
        self.time.advance(3001)
        self.instance.detect_obstacle()

        self.assertFalse(self.instance.is_remembering_obstacle)

    def test_remember_obstacle_for_given_time(self):
        self.instance.is_remembering_obstacle = True

        self.sensor.set_distance(4000)

        self.instance.detect_obstacle()

        self.assertTrue(self.instance.is_remembering_obstacle)
        self.assertFalse(self.instance.is_seeing_obstacle)

        self.time.advance(2999)

        self.instance.detect_obstacle()

        self.assertTrue(self.instance.is_remembering_obstacle)
        self.assertFalse(self.instance.is_seeing_obstacle)

        self.time.advance(1)

        self.instance.detect_obstacle()

        self.assertFalse(self.instance.is_remembering_obstacle)
        self.assertFalse(self.instance.is_seeing_obstacle)

    def test_recognising_obstacle(self):
        self.sensor.set_distance(5)
        self.instance.detect_obstacle()

        self.assertTrue(self.instance.is_seeing_obstacle)
        self.assertFalse(self.instance.is_recognising_obstacle)

        self.time.advance(51)

        self.instance.detect_obstacle()
        self.assertTrue(self.instance.is_seeing_obstacle)
        self.assertTrue(self.instance.is_recognising_obstacle)
        
    def test_seeing_but_not_yet_recognising_obstacle(self):
        self.sensor.set_distance(5)
        self.instance.detect_obstacle()

        self.assertTrue(self.instance.is_seeing_obstacle)
        self.assertFalse(self.instance.is_recognising_obstacle)

        self.time.advance(49)

        self.instance.detect_obstacle()
        self.assertTrue(self.instance.is_seeing_obstacle)
        self.assertFalse(self.instance.is_recognising_obstacle)
        
    def test_forget_recognising_obstacle(self):
        self.sensor.set_distance(5)
        self.instance.detect_obstacle()

        self.time.advance(51)

        self.instance.detect_obstacle()
        self.assertTrue(self.instance.is_recognising_obstacle)

        self.sensor.set_distance(100)
        self.instance.detect_obstacle()
        self.assertTrue(self.instance.is_recognising_obstacle)

        self.time.advance(51)

        self.instance.detect_obstacle()
        self.assertFalse(self.instance.is_recognising_obstacle)



if __name__ == '__main__':
    unittest.main()
