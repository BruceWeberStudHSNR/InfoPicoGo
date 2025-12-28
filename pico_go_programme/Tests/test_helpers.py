import os
import sys
from unittest.mock import Mock

# Ensure repository root (Info) is importable when running tests so
# package imports like `from AutoPicoGo import AutoPicoGo` work.
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Provide a small fake `machine` module when running on CPython so hardware
# modules that import `machine.Pin` / `machine.PWM` don't fail during tests.
if 'machine' not in sys.modules:
    import types

    class _Pin:
        OUT = 0
        IN = 1

        def __init__(self, pin, mode=None):
            self._val = 0

        def value(self, v=None):
            if v is None:
                return self._val
            self._val = v

    class _PWM:
        def __init__(self, pin):
            self._pin = pin

        def freq(self, f):
            return None

        def duty_u16(self, v):
            return None

    fake_machine = types.SimpleNamespace(Pin=_Pin, PWM=_PWM)
    sys.modules['machine'] = fake_machine

# Provide a minimal fake `rp2` module for tests so PIO-related imports don't fail on CPython.
if 'rp2' not in sys.modules:
    import types

    def asm_pio(*dargs, **dkwargs):
        # decorator that returns the function unchanged
        def _decor(f):
            return f
        return _decor

    class _PIO:
        OUT_LOW = 0
        SHIFT_LEFT = 0

    class _StateMachine:
        def __init__(self, id, asm, freq=0, sideset_base=None, out_base=None, in_base=None):
            self._buf = []

        def active(self, val):
            return None

        def put(self, val):
            # simulate putting value into buffer
            self._buf.append(val)

        def get(self):
            # return a default value
            if self._buf:
                return self._buf.pop(0)
            return 0

    fake_rp2 = types.SimpleNamespace(asm_pio=asm_pio, PIO=_PIO, StateMachine=_StateMachine)
    sys.modules['rp2'] = fake_rp2

# Provide a small fake `utime` module mapping to Python's time (ticks_ms, sleep_ms)
if 'utime' not in sys.modules:
    import types
    import time as _time

    def _ticks_ms():
        return int(_time.time() * 1000)

    def _sleep_ms(ms):
        _time.sleep(ms / 1000.0)

    fake_utime = types.SimpleNamespace(ticks_ms=_ticks_ms, sleep_ms=_sleep_ms)
    sys.modules['utime'] = fake_utime


class TimeServiceStub:
    def __init__(self, start=0):
        self._time = start

    def ticks_ms(self):
        return self._time

    def advance(self, ms):
        self._time += ms
        print ("advance",self._time)
        
    def set_ticks_ms(self, t):
        self._time = t


class SensorStub:
    def __init__(self, distance=100):
        self._distance = distance

    def get_distance(self):
        return self._distance

    def set_distance(self, d):
        self._distance = d


class BuzzerStub:
    def __init__(self):
        self._on = False

    def on(self):
        self._on = True

    def off(self):
        self._on = False

    def is_on(self):
        return self._on
    
class IRSensorStub:
    def __init__(self, position=2000, sensor_values=None):
        self._position = position
        if sensor_values is None:
            sensor_values = [0, 0, 0, 0, 0]
        self._sensor_values = sensor_values

    def readLine(self):
        return self._position, self._sensor_values

    def set_line_position(self, position):
        self._position = position

    def set_sensor_values(self, values):
        self._sensor_values = values


def mock_hardware():
    """Create an AutoPicoGo instance wired with stubs for quick tests.

    Returns (motor_stub, us_stub, time_stub, buzzer_stub, ir_sensor_stub)
    """
    
    motor = MotorStub()
    us = SensorStub(distance=100)
    time_svc = TimeServiceStub(0)
    buzzer = BuzzerStub()
    ir_sensor = IRSensorStub()

    # pass hardware instances; AutoPicoGo will instantiate services using them
    return motor, us, time_svc, buzzer, ir_sensor

class MockLineFollowService():
    def __init__(self, IRSensor, Motor, forward_speed):
        self.__last_line_position = 0
        self.__IRSensor = IRSensor
        self.__Motor = Motor
        self.forward_speed = forward_speed
        self.__on_line = False
        self.__line_state = "SEARCHING"
        
    follow_line = Mock()
    search_for_line = Mock()
    line_position_to_motor_power = Mock()
    is_on_line = Mock(return_value=False)
    
    def get_line_state(self):
        return self.__line_state

        
class MockAvoidObstacleService():
    def __init__(self, USSensor,TimeService, Motor, turn_speed, forward_speed, ):
        self.is_remembering_obstacle = False
        self.__USSensor = USSensor
        self.__Motor = Motor
        self.turn_speed = turn_speed
        self.forward_speed = forward_speed
        self.__TimeService = TimeService
        self.scan_and_avoid_obstacle = Mock(return_value=None)
        self.drive_around_obstacle = Mock()
        