class MockMotor:
    def __init__(self):
        self.commands = []
        
    def setMotor(self, left, right):
        self.commands.append(f"SET_MOTOR({left}, {right})")
        
    def stop(self):
        self.commands.append("STOP")
        
    def forward(self, speed):
        self.commands.append(f"FORWARD {speed}")
        
    def right(self, speed):
        self.commands.append(f"RIGHT {speed}")

    def left(self, speed):
        self.commands.append(f"LEFT {speed}")
        
    def backward(self, speed):
        self.commands.append(f"BACKWARD {speed}")
        
    def get_last_action(self):
        if self.commands == []:
            return None
        return self.commands[-1]