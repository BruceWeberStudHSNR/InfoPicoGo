
from Motor import MotorControl
from TRSensor import TRSensor
from machine import Pin
from UltraSoundSensor import UltraSoundSensor
from pico_go_programme.UltraSoundObstacleService import UltraSoundObstacleService


class AutoPicoGo():
    def __init__(self,forward_speed = 50, 
                 turn_speed = 25,
                 is_checking_for_obstacles=True):
        self.forward_speed = forward_speed
        self.turn_speed = turn_speed
        
        self.__car_action = "IDLE" #"FOLLOW_LINE" # / "DRIVE_AROUND_OBSTACLE" / "RETURN_TO_LINE" 
        self.is_checking_for_obstacles=is_checking_for_obstacles

        self.__Motor = MotorControl()
        self.__IRSensor = TRSensor()
        self.__USSensor = UltraSoundSensor()
        self.__BuzzerPin = Pin(4, Pin.OUT)

        self.__UltraSoundObstacleService = UltraSoundObstacleService(self.__USSensor) 

    def drive(self):
        if (self.__car_action == "IDLE"):
            # maybe check for controller change when implemented
            pass
        elif(self.__car_action == "FOLLOW_LINE"):
            self.__follow_line()
            pass
        elif(self.is_checking_for_obstacles and self.__car_action == "DRIVE_AROUND_OBSTACLE"):
            pass

    def __follow_line(self):
        if (self.is_checking_for_obstacles and self.__USSensor.get_distance()):


    def __check_for_obstacle(self):
        pass


