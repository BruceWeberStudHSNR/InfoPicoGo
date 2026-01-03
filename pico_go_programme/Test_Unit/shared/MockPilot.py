
from Hardware_Mocks.MockMotor import MockMotor

class MockPilot:
    def __init__(self, Motor=None, TimeService=None):
        self.mockMotor = Motor if Motor else MockMotor()
        self.current_speed = 0
        self.current_direction = "STOP"  # Possible directions: "FORWARD", "BACKWARD", "LEFT", "RIGHT", "STOP"
        self.default_speed = 50
        self.speed_levels = [20, 40, 60, 80, 100]
        self.has_stopped = False
    
    def set_speed(self, speed):
        self.default_speed = speed
        
    def __use_speed_or_default(self, speed):
        if speed is None or speed <= 0:
            return self.default_speed
        return speed
        
    def stop(self):
        self.mockMotor.stop()
        self.current_direction = "STOP"
        self.current_speed = 0
        self.has_stopped = True

    def go_direction_for_ms(self, direction, duration_ms, speed=None):
        speed = self.__use_speed_or_default(speed)
        self.go(direction, speed)
        # Note: Time-based logic is not simulated in this mock; tests handle time manually
        
    def set_wheels_for_ms(self, left_speed, right_speed, duration_ms):
        self.set_wheels(left_speed, right_speed)
        # Note: Time-based logic is not simulated in this mock
    
    def go(self, direction, speed=None):
        speed = self.__use_speed_or_default(speed)
        self.current_direction = direction
        self.current_speed = speed
        
        if direction == "LEFT":
            self.left(speed)
        elif direction == "RIGHT":
            self.right(speed)
        elif direction == "FORWARD":
            self.forward(speed)
        elif direction == "BACKWARD":
            self.backward(speed)
        else:
            self.stop()
            
    def forward(self, speed=None):
        speed = self.__use_speed_or_default(speed)
        self.mockMotor.forward(speed)
        self.current_direction = "FORWARD"
        self.current_speed = speed

    def backward(self, speed=None):
        speed = self.__use_speed_or_default(speed)
        self.mockMotor.backward(speed)
        self.current_direction = "BACKWARD"
        self.current_speed = speed
        
    def right(self, speed=None):
        speed = self.__use_speed_or_default(speed)
        self.mockMotor.right(speed)
        self.current_direction = "RIGHT"
        self.current_speed = speed

    def left(self, speed=None):
        speed = self.__use_speed_or_default(speed)
        self.mockMotor.left(speed)
        self.current_direction = "LEFT"
        self.current_speed = speed
        
    def set_wheels(self, left_speed, right_speed):
        self.mockMotor.setMotor(left_speed, right_speed)
        self.current_direction = "SET_WHEELS"
        self.current_speed = 0  # Not applicable
        
    def get_state(self):
        return self.current_direction
        
    def get_last_action(self):
        return self.mockMotor.get_last_action()