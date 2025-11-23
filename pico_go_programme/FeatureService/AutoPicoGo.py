
from Info.pico_go_programme.Hardware import TRSensor,MotorControl, UltraSoundSensor, Buzzer
import time
from Info.pico_go_programme.FeatureService import AvoidObstacleService, LineFollowService


class AutoPicoGo():
    def __init__(self, forward_speed=50, turn_speed=25, is_checking_for_obstacles=True,
                 motor=None, ir_sensor=None, us_sensor=None, buzzer=None, time_service=None, line_follow_service=None, avoid_obstacle_service=None):
        # basic settings
        self.forward_speed = forward_speed
        self.turn_speed = turn_speed
        self.is_checking_for_obstacles = is_checking_for_obstacles
        self.__automated_car_action = "FOLLOW_LINE"

        # --- 1) instantiate hardware components (clean, readable) ---
        self.__Motor = motor if motor is not None else MotorControl()
        self.__IRSensor = ir_sensor if ir_sensor is not None else TRSensor()
        self.__USSensor = us_sensor if us_sensor is not None else UltraSoundSensor()
        self.__Buzzer = buzzer if buzzer is not None else Buzzer()
        # --- 2) instantiate services, passing hardware instances ---
        self.__TimeService = time_service if time_service is not None else time
        self.__LineFollowService = line_follow_service if line_follow_service is not None else LineFollowService(self.__IRSensor, self.__Motor, self.forward_speed)
        self.__AvoidObstacleService = avoid_obstacle_service if avoid_obstacle_service is not None else AvoidObstacleService(self.__USSensor, self.__Motor, self.turn_speed, self.forward_speed, self.__TimeService)

    def automated_drive(self):
        if (self.__automated_car_action == "IDLE"):
            self.idle()
            pass
        elif(self.__automated_car_action == "FOLLOW_LINE"):
            self.follow_line()
            pass
        elif(self.__automated_car_action == "DRIVE_AROUND_OBSTACLE"):
            self.drive_around_obstacle()
            pass
        
    def set_automated_car_action(self, action):
        self.__automated_car_action = action

    def idle(self):
        self.__Motor.setMotor(0,0)
            
    def follow_line(self):
        if (self.is_checking_for_obstacles):
            self.__check_for_obstacle()
            

        self.__LineFollowService.follow_line_with_search()
        
    def drive_around_obstacle(self):
          # Check if line is visible again
          # Probably will not work as intended as you need to leave to line to avoid the obstacle
        if (self.__LineFollowService.is_on_line() or not self.__AvoidObstacleService.is_remembering_obstacle):
            self.__automated_car_action = "FOLLOW_LINE"
        else:
            self.__AvoidObstacleService.drive_around_obstacle()

    def __check_for_obstacle(self):
        if ( self.is_checking_for_obstacles):       
            self.__AvoidObstacleService.scan_and_avoid_obstacle()
            if (self.__AvoidObstacleService.is_remembering_obstacle):
                self.__automated_car_action = "DRIVE_AROUND_OBSTACLE"
            
    def update_buzzer(self):
        if (self.__Buzzer.is_on()):
            self.__Buzzer.off()
