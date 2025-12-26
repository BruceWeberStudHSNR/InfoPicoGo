

from helper import has_time_elapsed


class PicoPilot:
    def __init__(self, Motor=None, TimeService=None, default_speed=50):
        self.__Motor = Motor
        self.__TimeService = TimeService
        self.__default_speed = default_speed

        self.__current_action = "FORWARD" # "FORWARD" / "RIGHT" / "STOP" / "LEFT" / "BACKWARD"
        self.__current_state_start_time = 0
        
    def set_speed(self, speed):
        self.__default_speed = speed
        
    def __update_action(self, new_action):
        current_time = self.__TimeService.ticks_ms()
        if (self.__current_action != new_action):
            self.__current_state_start_time = current_time
            self.__current_action = new_action

        return current_time
    
    def __use_speed_or_default(self, speed):
        if speed is None:
            return self.__default_speed
        return speed
        
    def stop(self):
        self.__Motor.stop()
        self.__update_action("STOP")


    def go_direction_for_ms(self, direction, duration_ms, speed=None):
        speed = self.__use_speed_or_default(speed)
        current_time = self.__update_action(direction)
        self.go(direction, speed)

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
        
    def get_state(self):
        return self.__current_action