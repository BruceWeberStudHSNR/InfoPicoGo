import os
import sys
import unittest

# ensure repo root is on sys.path when running this test directly
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)

# import local test helpers (they also ensure import paths are set up)
from pico_go_programme.Tests.test_helpers import TimeServiceStub, SensorStub

from pico_go_programme.AvoidObstacleService import AvoidObstacleService


class TestUltraSoundObstacleService(unittest.TestCase):
	def setUp(self):
		self.time = TimeServiceStub(start=0)
		self.sensor = SensorStub(distance=100)
		# use short times so tests run fast
		self.svc = AvoidObstacleService(self.sensor, self.time,
											 obstacle_forget_time=200,
											 obstacle_recognition_time=300,
											 obstacle_recognition_distance=20)

	# def test_is_obstacle_in_sight(self):
	# 	self.assertTrue(self.svc.is_obstacle_in_sight(20))
	# 	self.assertTrue(self.svc.is_obstacle_in_sight(0))
	# 	self.assertFalse(self.svc.is_obstacle_in_sight(21))

	def test_see_and_recognise_and_remember_flow(self):
		# initially no obstacle seen -> state should become NO_OBSTACLE
		# calling see_obstacle sets start time and state
		self.time._time = 1000
		self.svc.see_obstacle()
		self.assertEqual(self.svc.get_obstacle_state(), "OBSTACLE_IN_SIGHT")
		# not yet recognised
		self.svc.remember_obstacle()
		self.assertFalse(self.svc.is_remembering_obstacle)
		# advance past recognition time and recognise
		self.time.advance(400)
		self.svc.remember_obstacle()
		self.assertTrue(self.svc.is_remembering_obstacle)

	def test_forget_obstacle_resets_state_and_memory(self):
		# see obstacle
		self.time._time = 100
		self.svc.see_obstacle()
		self.time.advance(400)
		# mark remembered and then ensure forget clears it
		self.svc.remember_obstacle()
		self.assertTrue(self.svc.is_remembering_obstacle)
		# now advance beyond forget time and call forget
		self.time.advance(500)
		self.svc.forget_obstacle()
		self.assertFalse(self.svc.is_remembering_obstacle)
		self.assertEqual(self.svc.get_obstacle_state(), "NO_OBSTACLE")

	def test_scan_for_obstacle_triggers_see_when_in_sight(self):
		# sensor returns near distance -> should see obstacle
		self.sensor.set_distance(10)
		self.time._time = 50
		self.svc.scan_and_avoid_obstacle()
		self.assertEqual(self.svc.get_obstacle_state(), "OBSTACLE_IN_SIGHT")


if __name__ == '__main__':
	unittest.main()
