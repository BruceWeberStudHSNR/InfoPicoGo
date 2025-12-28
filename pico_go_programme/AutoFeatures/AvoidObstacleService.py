


import utime
from Hardware import LEDControl
from Helper.has_time_elapsed import has_time_elapsed
from AutoFeatures import UltraSoundObstacleDetection, PicoPilot


class AvoidObstacleService():
    def __init__(self, 
                TimeService,
                pilot,
                UltrasoundObstacleDetection,
                dash_time=1000):

        self.avoiding_state = "SEARCHING" # "SEARCHING" / "DRIVING" / "AVOIDING"
        self.__dash_time = dash_time
        
        self.__Pilot = pilot
        
        self.__TimeService = TimeService
        self.__dash_timer = self.__TimeService.ticks_ms()

        self.__UltraSoundObstacleDetection = UltrasoundObstacleDetection 
        
    def __update_avoiding_state(self, new_state):
        if (self.avoiding_state != new_state):
            self.avoiding_state = new_state
            self.__dash_timer = 0
            self.__Pilot.stop()
    
    def drive_around_obstacle(self):
        current_time = self.__TimeService.ticks_ms() # Get time after measurement, because of blocking ultrasonic measurement                                                                                                 


        if (self.avoiding_state == "SEARCHING"):
            self.turn_to_obstacle()
            
        elif (self.avoiding_state == "AVOIDING"):
            self.turn_away_from_obstacle()
            
        elif (self.avoiding_state == "DRIVING"):
            self.drive_forward(current_time)

    def turn_to_obstacle(self):
        self.__Pilot.left(15)
                    
        if (self.__UltraSoundObstacleDetection.is_recognising_obstacle):
            self.__update_avoiding_state("AVOIDING")
            
    def turn_away_from_obstacle(self):
        self.__Pilot.go(direction="RIGHT", speed=15)

        if (not self.__UltraSoundObstacleDetection.is_recognising_obstacle):
            self.__update_avoiding_state("DRIVING")
            
    def drive_forward(self, current_time):
        print("driving forward", current_time, self.__dash_timer, self.__dash_time)
        if not has_time_elapsed(current_time, self.__dash_timer, self.__dash_time):
            self.__Pilot.forward()            
        else:
            self.__update_avoiding_state("SEARCHING")
        
            