


import utime
from Hardware import MotorControl, LEDControl
from helper import has_time_elapsed
from AutoFeatures import UltraSoundObstacleDetection


class AvoidObstacleService():
    def __init__(self, 
                UltraSoundSensor=None, 
                TimeService=None,
                motor=None,
                LedControl=None,
                UltrasoundObstacleDetection=None):
        
        self.__avoiding_state = "SEARCHING" # "SEARCHING" / "DRIVING" / "AVOIDING"
        self.__dash_time = 1000
        self.__dash_timer = 0

        self.__LEDControl = LedControl if LedControl is not None else LEDControl.LEDControl()
        self.__Motor = motor if motor is not None else MotorControl.MotorControl()
        self.__Sensor = UltraSoundSensor if UltraSoundSensor is not None else UltraSoundSensor.UltraSoundSensor()
        self.__TimeService = TimeService if TimeService is not None else utime

        self.__UltraSoundObstacleDetection = UltrasoundObstacleDetection if UltrasoundObstacleDetection is not None else UltraSoundObstacleDetection.UltraSoundObstacleDetection(self.__Sensor, self.__TimeService)
    
    def drive_around_obstacle(self):
        print("drive around obstacle", self.__avoiding_state)
        current_time = self.__TimeService.ticks_ms()

        print("avoiding state: ", self.__avoiding_state)
        if (self.__dash_timer == 0):
            self.__dash_timer = current_time

        if (self.__avoiding_state == "SEARCHING"):
            # self.__LEDControl.pixels_fill(self.__LEDControl.GREEN)
            self.turn_to_obstacle()
            
        elif (self.__avoiding_state == "AVOIDING"):
            # self.__LEDControl.pixels_fill(self.__LEDControl.BLUE)
            self.turn_away_from_obstacle()
            
        elif (self.__avoiding_state == "DRIVING"):
            # self.__LEDControl.pixels_fill(self.__LEDControl.YELLOW)
            self.drive_forward(current_time)

        # self.__LEDControl.pixels_show()
            
    def turn_to_obstacle(self):
        self.__Motor.right(10)
                    
        if (self.__UltraSoundObstacleDetection.is_seeing_obstacle):
            self.__avoiding_state = "AVOIDING"
            self.__dash_timer = 0
            
    def turn_away_from_obstacle(self):
        self.__Motor.left(10)
    
        if (not self.__UltraSoundObstacleDetection.is_seeing_obstacle):
            self.__avoiding_state = "DRIVING"
            self.__dash_timer = 0
            
    def drive_forward(self, current_time):
        if has_time_elapsed(current_time, self.__dash_timer, self.__dash_time):
            self.__Motor.forward(50)
            
        else:
            self.__avoiding_state = "SEARCHING"
            self.__dash_timer = 0
        
            