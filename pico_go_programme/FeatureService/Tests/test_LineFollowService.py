
import unittest

# Use the mock service provided by the test helpers (it provides the
# methods tested: `get_car_action`, `follow`, `stop`)
from Info.pico_go_programme.Tests.test_helpers import mock_hardware
from pico_go_programme.LineFollowService import LineFollowService



class TestLineFollowService(unittest.TestCase):  
    
    def setUp(self):
        # Create a LineFollowService instance with mocked dependencies
        #def __init__(self, IRSensor=None, Motor=None, forward_speed=0, time_service=None, dash_time=2000, turn_time=1000):
        self.motor, us, self.time_svc, buzzer, self.ir_sensor = mock_hardware()
        
        self.line_follow_service = LineFollowService(IRSensor=self.ir_sensor, time_service=self.time_svc, Motor=self.motor, forward_speed=100, dash_time=500, turn_time=300)
        
    def test_search_for_line_dashing(self):        
        self.line_follow_service.search_for_line()
        
        self.assertTrue(self.motor.forward.called)
        
    def test_search_for_line_turning(self):        
        # Simulate that dash time has passed to trigger turning
        self.line_follow_service.search_for_line()
        self.time_svc.advance(600)  # more than dash_time
        
        self.line_follow_service.search_for_line()
        self.line_follow_service.search_for_line()
        
        self.assertTrue(self.motor.right.called)
        
    
