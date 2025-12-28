from Helper.has_time_elapsed import has_time_elapsed

class UltraSoundObstacleDetection():
    def __init__(self, 
                 UltraSoundSensor = None,
                TimeService = None,
                obstacle_forget_time = 5000,
                obstacle_remember_time = 2000,
                obstacle_recognition_time = 500,
                obstacle_recognition_distance = 50,
                ):
        self.__obstacle_forget_time =  obstacle_forget_time
        self.__obstacle_remember_time =obstacle_remember_time
        self.__obstacle_recognition_time = obstacle_recognition_time
        self.__obstacle_recognition_distance =obstacle_recognition_distance
        
        # If the Obstacle is currently still in front of the auto
        self.is_seeing_obstacle = False 
        # Seeing but with a time buffer to avoid sensor noise
        self.is_recognising_obstacle = False
        # If the Obstacle was long enough in front of the auto to be recognised
        # And not long enough to be forgotten
        self.is_remembering_obstacle = False

        self.__Sensor = UltraSoundSensor
        self.__TimeService = TimeService
        self.__obstacle_time_counter =self.__TimeService.ticks_ms()

    def detect_obstacle(self):
        front_distance = self.scan_front_distance()
        current_time = self.__TimeService.ticks_ms()
        if (self.is_obstacle_in_sight(front_distance)):
            self.see_obstacle(current_time)
        else:
            self.forget_obstacle(current_time)


    def scan_front_distance(self):
        distance = self.__Sensor.get_distance()
        print("Distance measured", distance)
        return distance

    def is_obstacle_in_sight(self, distance):
        return distance <= self.__obstacle_recognition_distance

    def forget_obstacle(self, current_time):
        if (self.is_seeing_obstacle):
            self.__obstacle_time_counter = current_time
            self.is_seeing_obstacle = False
        else:
            if (has_time_elapsed(current_time, self.__obstacle_time_counter, self.__obstacle_recognition_time)):
                self.is_recognising_obstacle = False
            if (has_time_elapsed(current_time, self.__obstacle_time_counter,self.__obstacle_forget_time )):
                self.is_remembering_obstacle = False
    
    def see_obstacle(self, current_time):
        if (not self.is_seeing_obstacle):
            self.__obstacle_time_counter = current_time
            self.is_seeing_obstacle = True

        self.recognice_and_remember_obstacle(current_time)

    def recognice_and_remember_obstacle(self, current_time):
        if (has_time_elapsed(current_time, self.__obstacle_time_counter, self.__obstacle_recognition_time)):
            self.is_recognising_obstacle = True
        
        if (has_time_elapsed(current_time, self.__obstacle_time_counter, self.__obstacle_remember_time)):
            self.__obstacle_time_counter = current_time
            self.is_remembering_obstacle = True
