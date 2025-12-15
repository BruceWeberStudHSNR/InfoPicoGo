
from Hardware import MotorControl, TRSensor, UltraSoundSensor, Buzzer, LEDControl
from machine import Pin
from FeatureService import LineFollowService,AvoidObstacleService
import utime


class AutoPicoGo():
    def __init__(self, forward_speed=20, turn_speed=25, is_checking_for_obstacles=True,
                 motor=None, ir_sensor=None, us_sensor=None, buzzer=None, time_service=None, line_follow_service=None, avoid_obstacle_service=None, LedControl=None):
        
        self.forward_speed = forward_speed
        self.turn_speed = turn_speed
        
        self.__car_action = "FOLLOW_LINE" #"FOLLOW_LINE" # / "DRIVE_AROUND_OBSTACLE" / "RETURN_TO_LINE" 
        self.is_checking_for_obstacles=is_checking_for_obstacles

        self.__Motor = motor if motor is not None else MotorControl.MotorControl()
        self.__IRSensor = ir_sensor if ir_sensor is not None else TRSensor.TRSensor()
        self.__LedControl = LedControl if LedControl is not None else LEDControl.LEDControl()
        # self.__USSensor = us_sensor if us_sensor is not None else UltraSoundSensor.UltraSoundSensor()
        # self.__Buzzer = buzzer if buzzer is not None else Buzzer.Buzzer()
        # --- 2) instantiate services, passing hardware instances ---
        # self.__TimeService = time_service if time_service is not None else utime
        self.__LineFollowService = line_follow_service if line_follow_service is not None else LineFollowService.LineFollowService(self.__IRSensor, self.__Motor, self.forward_speed, self.__LedControl)
        # self.__AvoidObstacleService = avoid_obstacle_service if avoid_obstacle_service is not None else AvoidObstacleService.AvoidObstacleService(self.__USSensor, self.__TimeService, self.__Motor, 2000, 3000, 20 )

    def run(self):
        self.drive()

    def calibrate(self):
        print("Calibrate Start")
        for i in range(100):
            if(i<25 or i>= 75):
                self.__Motor.setMotor(30,-30)
            else:
                self.__Motor.setMotor(-30,30)
            self.__IRSensor.calibrate()

        print ("Calibrate End")

    def drive(self):
        # if (self.__car_action == "IDLE"):
        #     # maybe check for controller change when implemented
        #     pass
        # if(self.__car_action == "FOLLOW_LINE"):
        self.__follow_line()
        # elif(self.is_checking_for_obstacles and self.__car_action == "DRIVE_AROUND_OBSTACLE"):
        #     pass

    def __follow_line(self):
        self.__LineFollowService.follow_line_with_search()


    def __check_for_obstacle(self):
        pass



