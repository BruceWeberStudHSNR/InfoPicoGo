
class AvoidObstacleService():
    def __init__(self, 
                TimeService,
                pilot,
                UltrasoundObstacleDetection,
                dash_time=1000,
                minimum_turn_time= 500,
                max_search_time= 500):

        self.avoiding_state = "SEARCHING" # "SEARCHING" / "DRIVING" / "AVOIDING"
        self.__dash_time = dash_time
        self.__turn_start_time = 0
        self.__dynamic_turn_time = 0
        self.__minimum_turn_time = minimum_turn_time
        self.__max_search_time = max_search_time
        
        self.__Pilot = pilot
        
        self.__TimeService = TimeService
        self.__dash_timer = self.__TimeService.ticks_ms()

        self.__UltraSoundObstacleDetection = UltrasoundObstacleDetection 
        
    def __update_avoiding_state(self, new_state):
        if (self.avoiding_state != new_state):
            self.avoiding_state = new_state
            
            print("AvoidObstacleState changed to: ", new_state)
            print("dash_timer: ",self.__TimeService.elapsed_time(self.__dash_timer))
            print("distance:", self.__UltraSoundObstacleDetection.measured_distance)
            print("turn time:", self.__dynamic_turn_time)
            self.__Pilot.stop()

            if (new_state == "AVOIDING" or new_state == "SEARCHING"):
                self.__dynamic_turn_time = self.__TimeService.elapsed_time(self.__turn_start_time)
                self.__turn_start_time = self.__TimeService.ticks_ms()

            if (new_state == "DRIVING"):
                print("dash_timer: ",self.__TimeService.elapsed_time(self.__dash_timer))
                self.__dash_timer = self.__TimeService.ticks_ms()
    
    def drive_around_obstacle(self):
        if (self.avoiding_state == "SEARCHING"):
            self.search_obstacle()
            
        elif (self.avoiding_state == "AVOIDING"):
            self.turn_away_from_obstacle()
            
        elif (self.avoiding_state == "DRIVING"):
            self.drive_forward()

    def search_obstacle(self):  
        self.__Pilot.go(direction="LEFT")
        if (self.__UltraSoundObstacleDetection.is_recognising_obstacle or 
            not self.__UltraSoundObstacleDetection.is_remembering_obstacle or
            self.__TimeService.has_time_elapsed(self.__turn_start_time, self.__max_search_time)
            ):
            print ("seeing:",self.__UltraSoundObstacleDetection.is_remembering_obstacle," not remembering: ", not self.__UltraSoundObstacleDetection.is_remembering_obstacle)
            self.__update_avoiding_state("AVOIDING")
            
            
    def turn_away_from_obstacle(self):
        self.__Pilot.go(direction="RIGHT")
        
        if ((not self.__UltraSoundObstacleDetection.is_recognising_obstacle and self.__TimeService.has_time_elapsed(self.__turn_start_time, self.__dynamic_turn_time/2)) or self.__TimeService.has_time_elapsed(self.__turn_start_time, self.__max_search_time) ):
            self.__update_avoiding_state("DRIVING")

    def drive_forward(self):
        self.__Pilot.go("FORWARD")

        if (self.__UltraSoundObstacleDetection.is_recognising_obstacle):
            self.__update_avoiding_state("AVOIDING")

        elif (self.__TimeService.has_time_elapsed(self.__dash_timer,self.__dash_time)):
            self.__update_avoiding_state("SEARCHING")
        
            