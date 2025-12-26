
class MockPilot:
    def __init__(self):
        self.current_speed = 0
        self.current_direction = "STOP"  # Possible directions: "FORWARD", "BACKWARD", "LEFT", "RIGHT", "STOP"
    
    def go(self, direction, speed):
        self.current_direction = direction
        self.current_speed = speed
    
    def stop(self):
        self.current_direction = "STOP"
        self.current_speed = 0