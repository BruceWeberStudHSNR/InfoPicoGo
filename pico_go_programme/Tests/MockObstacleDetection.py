class MockObstacleDetection():
    def __init__(self, obstacle_forget_time = 2000, obstacle_recognition_time = 3000, obstacle_recognition_distance = 40 ):
        self.is_seeing_obstacle = False
        self.is_remembering_obstacle = False
        self.__front_distance = 0
        self.__obstacle_recognition_distance = obstacle_recognition_distance
        
    def detect_obstacle(self):
        pass
    
    def set_front_distance(self, distance):
        self.__front_distance = distance
        
    def scan_front_distance(self):
        return self.__front_distance
    
    def is_obstacle_in_sight(self, distance):
        return distance <= self.__obstacle_recognition_distance
    
    def forget_obstacle(self, current_time):
        self.is_seeing_obstacle = False
        self.is_remembering_obstacle = False
        
    def see_obstacle(self, current_time):
        self.is_seeing_obstacle = True
        self.is_remembering_obstacle = False
        
    def remember_obstacle(self, current_time):
        self.is_remembering_obstacle = True
        
    