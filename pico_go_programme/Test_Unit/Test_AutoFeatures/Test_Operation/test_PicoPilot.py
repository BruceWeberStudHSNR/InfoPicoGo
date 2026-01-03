
import unittest
from Test_Unit.shared import StubsAndMocks
from AutoFeatures.Operation import PicoPilot
from Hardware_Mocks import MockMotor

class TestPicoPilot(unittest.TestCase):
    def setUp(self):
        self.time_service = StubsAndMocks.TimeServiceStub(0)
        self.motor = MockMotor.MockMotor()
        self.pico_pilot = PicoPilot.PicoPilot(Motor=self.motor, TimeService=self.time_service)

    def test_go_forward(self):
        self.pico_pilot.go(speed=20, direction="FORWARD")
        self.assertEqual(self.motor.get_last_action(), "FORWARD 20")
        
    def test_go_backward(self):
        self.pico_pilot.go(speed=15, direction="BACKWARD")
        self.assertEqual(self.motor.get_last_action(), "BACKWARD 15")
        
    def test_go_direction_for_ms_forward(self):
        self.pico_pilot.go_direction_for_ms(speed=20, direction="FORWARD", duration_ms=1000)
        self.assertEqual(self.motor.get_last_action(), "FORWARD 20")
        self.time_service.advance(1001)
        self.pico_pilot.go_direction_for_ms(speed=20, direction="FORWARD", duration_ms=1000)
        self.assertEqual(self.motor.get_last_action(), "STOP")
        
    def test_go_direction_for_ms_right(self):
        self.pico_pilot.go_direction_for_ms( direction="RIGHT", duration_ms=500,speed=15)
        self.pico_pilot.go_direction_for_ms( direction="RIGHT", duration_ms=500,speed=15)
        self.assertEqual(self.motor.get_last_action(), "RIGHT 15")
        self.time_service.advance(501)
        self.pico_pilot.go_direction_for_ms(speed=15, direction="RIGHT", duration_ms=500)
        self.assertEqual(self.motor.get_last_action(), "STOP")
        
    def test_go_direction_for_ms_left(self):
        self.pico_pilot.go_direction_for_ms(speed=15, direction="LEFT", duration_ms=500)
        self.assertEqual(self.motor.get_last_action(), "LEFT 15")
        self.time_service.advance(501)
        self.pico_pilot.go_direction_for_ms(speed=15, direction="LEFT", duration_ms=500)
        self.assertEqual(self.motor.get_last_action(), "STOP")
        
    
        
    
