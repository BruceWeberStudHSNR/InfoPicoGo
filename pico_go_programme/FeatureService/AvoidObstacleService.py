


import utime
from Hardware import MotorControl, UltraSoundSensor
from helper import has_time_elapsed


class AvoidObstacleService():
    def __init__(self, 
                UltraSoundSensor=None, 
                TimeService=None,
                motor=None,
                obstacle_forget_time = 2000,
                obstacle_recognition_time = 3000,
                obstacle_recognition_distance = 20 ):
        
        
        # Obstacle Memory Service
        self.__obstacle_forget_time =  obstacle_forget_time
        self.__obstacle_recognition_time =obstacle_recognition_time
        self.__obstacle_recognition_start_time =0
        self.__obstacle_recognition_distance =obstacle_recognition_distance
        self.__obstacle_state = "NO_OBSTACLE"
        self.is_remembering_obstacle = False
        
        self.__avoiding_state = "SEARCHING" # "SEARCHING" / "DRIVING" / "AVOIDING"
        self.__dash_time = 2000
        self.__dash_timer = 0

        self.__Motor = motor if motor is not None else MotorControl()
        self.__Sensor = UltraSoundSensor if UltraSoundSensor is not None else UltraSoundSensor()
        self.__TimeService = TimeService if TimeService is not None else utime
        
    def is_obstacle_in_sight(self):
        distance = self.__Sensor.get_distance()
        print("is in sight distance", distance, distance <= self.__obstacle_recognition_distance)
        
        return distance <= self.__obstacle_recognition_distance

    def forget_obstacle(self):
        if (self.is_remembering_obstacle):
            current_time = self.__TimeService.ticks_ms()
            time_delta = current_time - self.__obstacle_recognition_start_time
            if (time_delta > self.__obstacle_forget_time):
                self.__obstacle_recognition_start_time = 0
                self.__obstacle_state = "NO_OBSTACLE"
                self.is_remembering_obstacle = False

    def see_obstacle(self):
        current_time = self.__TimeService.ticks_ms()
        self.__obstacle_recognition_start_time = current_time
        self.__obstacle_state = "OBSTACLE_IN_SIGHT"

    def remember_obstacle(self):
        current_time = self.__TimeService.ticks_ms()
        time_delta = current_time - self.__obstacle_recognition_start_time
        if (time_delta > self.__obstacle_recognition_time):
            self.is_remembering_obstacle = True
    
    def scan_and_avoid_obstacle(self):
        if (self.is_remembering_obstacle):
            if self.is_obstacle_in_sight():
                self.drive_around_obstacle()
            else:
                self.forget_obstacle()
        else:
            is_in_sight = self.is_obstacle_in_sight()
            if is_in_sight:
                if(self.__obstacle_state == "NO_OBSTACLE"):
                    self.see_obstacle()
                elif (self.__obstacle_state == "OBSTACLE_IN_SIGHT" and not self.is_remembering_obstacle):
                    self.remember_obstacle()
    
    def drive_around_obstacle(self):
        print("drive around obstacle", self.__avoiding_state)
        current_time = self.__TimeService.ticks_ms()
        
        if (self.__dash_timer == 0):
            self.__dash_timer = current_time

        if (self.__avoiding_state == "SEARCHING"):
            self.turn_to_obstacle()
            
        elif (self.__avoiding_state == "AVOIDING"):
            self.turn_away_from_obstacle()
            
        elif (self.__avoiding_state == "DRIVING"):
            self.drive_forward(current_time)
            
    def turn_to_obstacle(self):
        self.__Motor.right(25)
                    
        if (self.is_obstacle_in_sight()):
            self.__avoiding_state = "AVOIDING"
            self.__dash_timer = 0
            
    def turn_away_from_obstacle(self):
        self.__Motor.left(25)
        
        if (not self.is_obstacle_in_sight()):
            self.__avoiding_state = "DRIVING"
            self.__dash_timer = 0
            
    def drive_forward(self, current_time):
        if has_time_elapsed(current_time, self.__dash_timer, self.__dash_time):
            self.__Motor.forward(25)
        else:
            self.__avoiding_state = "SEARCHING"
            self.__dash_timer = 0
            
    def get_obstacle_state(self):
        return self.__obstacle_state
        
            