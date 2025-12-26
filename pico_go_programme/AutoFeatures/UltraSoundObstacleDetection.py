from helper import has_time_elapsed

class UltraSoundObstacleDetection():
    def __init__(self, 
                 UltraSoundSensor = None,
                TimeService = None,
                obstacle_forget_time = 2000,
                obstacle_recognition_time = 3000,
                obstacle_recognition_distance = 40 ):
        self.__obstacle_forget_time =  obstacle_forget_time
        self.__obstacle_recognition_time =obstacle_recognition_time
        self.__obstacle_recognition_start_time =0
        self.__obstacle_recognition_distance =obstacle_recognition_distance
        
        # If the Obstacle is currently still in front of the auto
        self.is_seeing_obstacle = False 
        # If the Obstacle was long enough in front of the auto to be recognised
        # And not long enough to be forgotten
        self.is_remembering_obstacle = False

        self.__Sensor = UltraSoundSensor
        self.__TimeService = TimeService

    def detect_obstacle(self):
        front_distance = self.scan_front_distance()
        current_time = self.__TimeService.ticks_ms()
        if (self.is_obstacle_in_sight(front_distance)):
            self.see_obstacle(current_time)
        else:
            self.forget_obstacle(current_time)


    def scan_front_distance(self):
        distance = self.__Sensor.get_distance()
        print("Distance", distance)
        return distance

    def is_obstacle_in_sight(self, distance):
        return distance <= self.__obstacle_recognition_distance

    def forget_obstacle(self, current_time):
        if (self.is_seeing_obstacle):
            self.__obstacle_recognition_start_time = current_time
            self.is_seeing_obstacle = False
        else:
            if (has_time_elapsed(current_time, self.__obstacle_recognition_start_time,self.__obstacle_forget_time )):
                    self.is_remembering_obstacle = False
    
    def see_obstacle(self, current_time):
        if (not self.is_seeing_obstacle):
            self.__obstacle_recognition_start_time = current_time
            self.is_seeing_obstacle = True

        self.remember_obstacle(current_time)

    def remember_obstacle(self, current_time):
        if (has_time_elapsed(current_time, self.__obstacle_recognition_start_time, self.__obstacle_recognition_time)):
            self.__obstacle_recognition_start_time = current_time
            self.is_remembering_obstacle = True

    def get_obstacle_state(self):
        return self.is_seeing_obstacle
