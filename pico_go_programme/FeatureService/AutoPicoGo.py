
from Hardware import MotorControl, TRSensor, UltraSoundSensor, Buzzer, LEDControl
from machine import Pin
from FeatureService import LineFollowService,AvoidObstacleService, UltraSoundObstacleDetection
import utime


class AutoPicoGo():
    def __init__(self, forward_speed=20, turn_speed=25, is_checking_for_obstacles=True,
                 motor=None, ir_sensor=None, us_sensor=None, buzzer=None, time_service=None, line_follow_service=None, avoid_obstacle_service=None, LedControl=None,UltrasoundObstacleDetection=None):
        
        self.forward_speed = forward_speed
        self.turn_speed = turn_speed
        
        self.__car_action = "FOLLOW_LINE" #"FOLLOW_LINE" # / "DRIVE_AROUND_OBSTACLE" / "RETURN_TO_LINE" 
        self.is_checking_for_obstacles=is_checking_for_obstacles

        self.__Motor = motor if motor is not None else MotorControl.MotorControl()
        self.__IRSensor = ir_sensor if ir_sensor is not None else TRSensor.TRSensor()
        self.__LedControl = LedControl if LedControl is not None else LEDControl.LEDControl()
        self.__USSensor = us_sensor if us_sensor is not None else UltraSoundSensor.UltraSoundSensor()
        # self.__Buzzer = buzzer if buzzer is not None else Buzzer.Buzzer()
        # --- 2) instantiate services, passing hardware instances ---
        self.__TimeService = time_service if time_service is not None else utime
        self.__LineFollowService = line_follow_service if line_follow_service is not None else LineFollowService.LineFollowService(self.__IRSensor, self.__Motor, self.forward_speed,self.__TimeService, 2000, 1000, self.__LedControl)
        self.__UltraSoundObstacleDetection = UltrasoundObstacleDetection if UltrasoundObstacleDetection is not None else UltraSoundObstacleDetection.UltraSoundObstacleDetection(self.__USSensor, self.__TimeService)        
        self.__AvoidObstacleService = avoid_obstacle_service if avoid_obstacle_service is not None else AvoidObstacleService.AvoidObstacleService(self.__USSensor, self.__TimeService, self.__Motor, self.__LedControl, self.__UltraSoundObstacleDetection )

    def run(self):
        self.drive()

        self.update()

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
        print("Car Action: ",self.__car_action)
        if (self.is_checking_for_obstacles):
            self.__UltraSoundObstacleDetection.detect_obstacle()
            if (self.__UltraSoundObstacleDetection.is_seeing_obstacle):
                self.__LedControl.pixels_fill(self.__LedControl.RED)
            else:
                self.__LedControl.pixels_fill(self.__LedControl.GREEN)
        self.__LedControl.pixels_show()

        if(self.__car_action == "FOLLOW_LINE"):
            self.__follow_line()
        elif(self.__car_action == "DRIVE_AROUND_OBSTACLE"):
            self.__drive_around_obstacle()

    def __follow_line(self):
        
        if (self.__UltraSoundObstacleDetection.is_remembering_obstacle):
            self.__car_action = "DRIVE_AROUND_OBSTACLE"
        else:
            self.__LineFollowService.follow_line_with_search()

        
    def __drive_around_obstacle(self):
            print("Is on Line", self.__LineFollowService.is_on_line())
            if (self.__LineFollowService.is_on_line()):
                self.__car_action = "FOLLOW_LINE"
            else:
                self.__AvoidObstacleService.drive_around_obstacle()

    def update(self):
        self.update_leds()

    def update_leds(self):
        self.__LedControl.pixels_show()
