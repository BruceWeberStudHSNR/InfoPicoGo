
class UltraSoundObstacleService():

    def __init__(self, UltraSoundSensor, TimeService,
                 obstacle_forget_time = 2000,
                obstacle_recognition_time = 3000,
                obstacle_recognition_distance = 20 ):
        self.__obstacle_forget_time =  obstacle_forget_time
        self.__obstacle_recognition_time =obstacle_recognition_time
        self.__obstacle_recognition_start_time =0
        self.__obstacle_recognition_distance =obstacle_recognition_distance
        self.__obstacle_state == "NO_OBSTACLE"
        self.__remember_obstacle = False

        self.__Sensor = UltraSoundSensor
        self.__TimeService = TimeService

    def is_obstacle_in_sight(self, distance):
        return distance <= self.__obstacle_recognition_distance

    def forget_obstacle(self):
        self.__obstacle_recognition_start_time = 0
        self.__obstacle_state = "NO_OBSTACLE"

    def see_obstacle(self):
        current_time = self.__TimeService.ticks_ms()
        self.__obstacle_recognition_start_time = current_time
        self.__obstacle_state = "OBSTACLE_IN_SIGHT"

    def recognise_obstacle(self):
        current_time = self.__TimeService.ticks_ms()
        time_delta = current_time - self.__obstacle_recognition_start_time
        if (time_delta > self.__obstacle_recognition_time):
            self.__remember_obstacle = True

    def get_obstacle_state(self):
        return self.__obstacle_state

    def reset_recognition_timer(self):
        self.__obstacle_recognition_start_time = 0
    
    def scan_for_obstacle(self):
        
        measured_distance = self.__Sensor.get_distance()

        if self.is_obstacle_in_sight(measured_distance):
            if(self.__obstacle_state == "NO_OBSTACLE"):
                self.see_obstacle()
            elif (self.__obstacle_state = "OBSTACLE_IN_SIGHT"):
                self.recognise_obstacle()