       
        
# Unit tests for AutoPicoGo
import os
import sys
import unittest

# Ensure repository root (Info) is on sys.path so package imports work
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


from Info.pico_go_programme.AutoPicoGo import AutoPicoGo

from Info.pico_go_programme.Tests.test_helpers import MockAvoidObstacleService, MockLineFollowService, mock_hardware

class TestAutoPicoGo(unittest.TestCase):
    def test_auto_initializes_with_stubs(self):
        motor, us, time_svc, buzzer, ir_sensor = mock_hardware()
        # assert that AutoPicoGo was created and has expected internals
        auto = AutoPicoGo(motor=motor, us_sensor=us, buzzer=buzzer, time_service=time_svc)
        self.assertIsNotNone(auto)
        # example: drive() is callable
        self.assertTrue(hasattr(auto, 'automated_drive'))
        
    def test_auto_follows_line(self):
        motor, us, time_svc, buzzer, ir_sensor = mock_hardware()
        mock_line_service = MockLineFollowService(ir_sensor, motor, 50)
        mock_obstacle_service = MockAvoidObstacleService(us,time_svc, motor, 25, 50)
        
        auto = AutoPicoGo(motor=motor, 
                          us_sensor=us, 
                          buzzer=buzzer, 
                          time_service=time_svc, 
                          is_checking_for_obstacles=False, 
                          line_follow_service=mock_line_service, 
                          avoid_obstacle_service=mock_obstacle_service)
        
        # Mock response for mock_obstacle_service.check_for_obstacle to do nothing
        
        auto.automated_drive()
        # Check that LinefollowService was invoked to follow line
        mock_line_service.follow_line.assert_called()                   # a call happened