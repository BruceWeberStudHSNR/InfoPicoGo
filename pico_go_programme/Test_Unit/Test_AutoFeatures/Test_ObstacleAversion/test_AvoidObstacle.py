
import unittest

from Test_Unit.shared import StubsAndMocks, MockPilot
from AutoFeatures.ObstacleAversion import AvoidObstacleService
from Hardware_Mocks import MockMotor, MockUltraSoundSensor

class TestAvoidObstacle(unittest.TestCase):
    def setUp(self):
        print("="*20)
        self.time_service = StubsAndMocks.TimeServiceStub(0)
        self.motor = MockMotor.MockMotor()
        self.ultrasound_sensor = MockUltraSoundSensor.MockUltraSoundSensor()
        
        self.pico_pilot = MockPilot.MockPilot(
            Motor=self.motor, 
            TimeService=self.time_service)
        
        self.pico_pilot.set_speed(50)
        
        self.ultrasound_detection = StubsAndMocks.MockObstacleDetection(
            obstacle_forget_time=100, 
            obstacle_recognition_time=200, 
            obstacle_recognition_distance=20)
        
        self.avoid_obstacle_service = AvoidObstacleService.AvoidObstacleService(
            TimeService=self.time_service,
            pilot=self.pico_pilot,  # You may need to create a mock PicoPilot if required
            UltrasoundObstacleDetection=self.ultrasound_detection,
            dash_time=1000
        )

    def test_drive_around_obstacle_searching_to_avoiding(self):
        self.avoid_obstacle_service.avoiding_state = "SEARCHING"
        self.avoid_obstacle_service.drive_around_obstacle()
        self.assertEqual(self.motor.get_last_action(), "LEFT 50")
        self.assertEqual(self.avoid_obstacle_service.avoiding_state, "SEARCHING")
        
        self.ultrasound_detection.is_seeing_obstacle = True
        
        self.avoid_obstacle_service.drive_around_obstacle()
        self.assertEqual(self.avoid_obstacle_service.avoiding_state, "AVOIDING")
        
    def test_drive_around_obstacle_searching_staying(self):
        self.avoid_obstacle_service.avoiding_state = "SEARCHING"
        self.ultrasound_detection.is_seeing_obstacle = False
        
        self.avoid_obstacle_service.drive_around_obstacle()
        self.assertEqual(self.motor.get_last_action(), "LEFT 50")
        self.assertEqual(self.avoid_obstacle_service.avoiding_state, "SEARCHING")
        
        
    def test_drive_around_obstacle_avoiding_to_driving(self):
        self.avoid_obstacle_service.avoiding_state = "AVOIDING"
        self.ultrasound_detection.is_seeing_obstacle = False
        
        self.avoid_obstacle_service.drive_around_obstacle()
        self.assertEqual(self.avoid_obstacle_service.avoiding_state, "DRIVING")

    def test_drive_around_obstacle_driving_duration(self):
        self.avoid_obstacle_service.avoiding_state = "DRIVING"
        self.ultrasound_detection.is_seeing_obstacle = False

        self.avoid_obstacle_service.drive_around_obstacle()
        self.assertEqual(self.avoid_obstacle_service.avoiding_state, "DRIVING")

        self.time_service.advance(999)
        self.avoid_obstacle_service.drive_around_obstacle()

        self.assertEqual(self.avoid_obstacle_service.avoiding_state, "DRIVING")

        self.time_service.advance(2)
        self.avoid_obstacle_service.drive_around_obstacle()
        self.assertNotEqual(self.avoid_obstacle_service.avoiding_state, "DRIVING")


        
    def test_drive_around_obstacle_avoiding_staying(self):
        self.avoid_obstacle_service.avoiding_state = "AVOIDING"
        self.ultrasound_detection.is_seeing_obstacle = True
        
        self.avoid_obstacle_service.drive_around_obstacle()
        self.assertEqual(self.motor.get_last_action(), "RIGHT 50")
        self.assertEqual(self.avoid_obstacle_service.avoiding_state, "AVOIDING")
        
    def test_drive_around_obstacle_driving_to_searching(self):
        self.avoid_obstacle_service.avoiding_state = "DRIVING"
        self.ultrasound_detection.is_seeing_obstacle = False
        
        self.avoid_obstacle_service.drive_around_obstacle()
        self.assertEqual(self.motor.get_last_action(), "FORWARD 50")
        self.assertEqual(self.avoid_obstacle_service.avoiding_state, "DRIVING")
        
        self.time_service.advance(1001)  # Advance time to exceed dash_time
        self.avoid_obstacle_service.drive_around_obstacle()
        self.assertEqual(self.avoid_obstacle_service.avoiding_state, "SEARCHING")
        
    def test_cycle_searching_avoiding_driving(self):
        # Start in SEARCHING
        self.avoid_obstacle_service.avoiding_state = "SEARCHING"
        self.ultrasound_detection.is_seeing_obstacle = True
        
        self.avoid_obstacle_service.drive_around_obstacle()
        self.assertEqual(self.avoid_obstacle_service.avoiding_state, "AVOIDING")
        
        self.ultrasound_detection.is_seeing_obstacle = False
        self.avoid_obstacle_service.drive_around_obstacle()
        self.assertEqual(self.avoid_obstacle_service.avoiding_state, "DRIVING")
        
        self.time_service.advance(1001)  # Advance time to exceed dash_time
        self.avoid_obstacle_service.drive_around_obstacle()
        self.assertEqual(self.avoid_obstacle_service.avoiding_state, "SEARCHING")