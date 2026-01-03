

from Helper.has_time_elapsed import has_time_elapsed


class PicoPilot:
    def __init__(self, 
                 Motor, 
                 TimeService, 
                 default_speed=50,
                 speed_levels=[20, 40, 60, 80, 100]):
        self.__Motor = Motor
        self.__TimeService = TimeService
        self.default_speed = default_speed
        self.speed_levels = speed_levels
        self.__current_action = "FORWARD" # "FORWARD" / "RIGHT" / "STOP" / "LEFT" / "BACKWARD" / "SET_WHEELS"
        self.__current_state_start_time = 0
        self.has_stopped = False
        
    def set_speed(self, speed):
        self.default_speed = speed
        
    def __update_action(self, new_action):
        current_time = -1
        if (self.__current_action != new_action):
            self.__current_state_start_time = self.__TimeService.ticks_ms()
            self.__current_action = new_action
            
        self.has_stopped = new_action == "STOP"
        
        return current_time
    
    def __use_speed_or_default(self, speed):
        if speed is None or speed <= 0:
            return self.default_speed
        return speed
        
    def stop(self):
        self.__Motor.stop()
        self.__update_action("STOP")
        self.has_stopped = True


    def go_direction_for_ms(self, direction, duration_ms, speed=None):
        speed = self.__use_speed_or_default(speed)
        current_time = self.__update_action(direction)
        if (self.__TimeService.has_time_elapsed(self.__current_state_start_time, duration_ms)):
            self.stop()
        else:
            self.go(direction, speed)

        
    def set_wheels_for_ms(self, left_speed, right_speed, duration_ms):
        current_time = self.__update_action("SET_WHEELS")
        self.set_wheels(left_speed, right_speed)
    
        if has_time_elapsed(current_time, self.__current_state_start_time, duration_ms):
            self.stop()
            pass
        
    def go(self, direction, speed=None):
        speed = self.__use_speed_or_default(speed)
        
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
            assert False, "Unknown direction command"
            
    def forward(self, speed=None):
        speed = self.__use_speed_or_default(speed)
        self.__Motor.forward(speed)
        self.__update_action("FORWARD")

    def backward(self, speed=None):
        speed = self.__use_speed_or_default(speed)
        self.__Motor.backward(speed)
        self.__update_action("BACKWARD")
        
    def right(self, speed=None):
        speed = self.__use_speed_or_default(speed)
        self.__Motor.right(speed)
        self.__update_action("RIGHT")

    def left(self, speed=None):
        speed = self.__use_speed_or_default(speed)
        self.__Motor.left(speed)
        self.__update_action("LEFT")
        
    def set_wheels(self, left_speed, right_speed):
        self.__Motor.setMotor(left_speed, right_speed)
        self.__update_action("SET_WHEELS")

    def get_state(self):
        return self.__current_action