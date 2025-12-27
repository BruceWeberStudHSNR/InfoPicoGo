from Hardware import MotorControl, TRSensor, UltraSoundSensor, LEDControl
from machine import Pin
from AutoFeatures import LineFollowService,AvoidObstacleService, UltraSoundObstacleDetection, PicoPilot
import utime


class AutoPicoGo():
    def __init__(self,
                 Motor,
                 Tr_sensor,
                 Led,
                 Ultra_sound,
                 Buzzer,
                 forward_speed=20, 
                 turn_speed=15, 
                 is_checking_for_obstacles=True):
        self.forward_speed = forward_speed
        self.turn_speed = turn_speed
        
        self.__car_action = "FOLLOW_LINE" #"FOLLOW_LINE" # / "DRIVE_AROUND_OBSTACLE" / "RETURN_TO_LINE" 
        self.is_checking_for_obstacles=is_checking_for_obstacles

        # Use passed Hardware classes or instantiate default
        self.__Motor = Motor 
        self.__IRSensor = Tr_sensor 
        self.__LedControl = Led
        self.__USSensor = Ultra_sound
        self.__Buzzer = Buzzer 

        self.__Pilot = PicoPilot.PicoPilot(
            Motor=self.__Motor,
            TimeService=utime
        )
        # self.__Buzzer = buzzer if buzzer is not None else Buzzer.Buzzer()
        # --- 2) instantiate services, passing hardware instances ---
        self.__TimeService = utime
        self.__LineFollowService = LineFollowService.LineFollowService(
            IRSensor=self.__IRSensor, 
            Motor=self.__Motor, 
            forward_speed=self.forward_speed,
            TimeService=self.__TimeService, 
            dash_time=2000, 
            turn_time=1000)
        self.__UltraSoundObstacleDetection = UltraSoundObstacleDetection.UltraSoundObstacleDetection(
            self.__USSensor, 
            self.__TimeService)        
        self.__AvoidObstacleService = AvoidObstacleService.AvoidObstacleService(
            self.__USSensor, 
            self.__TimeService, 
            self.__Motor, 
            self.__LedControl, 
            self.__UltraSoundObstacleDetection )


    def run(self):        
        self.drive()

        self.update()

    def calibrate_line_sensors(self):
        print("Calibrate Start")
        for i in range(100):
            if(i<25 or i>= 75):
                self.__Motor.setMotor(30,-30)
            else:
                self.__Motor.setMotor(-30,30)
            self.__IRSensor.calibrate()

        print ("Calibrate End")
            
    def drive(self):
        if(self.__car_action == "FOLLOW_LINE"):
            self.follow_line()
        elif(self.__car_action == "DRIVE_AROUND_OBSTACLE"):
            self.drive_around_obstacle()

    def follow_line(self):
        self.__LineFollowService.detect_line()
        
        if (self.__UltraSoundObstacleDetection.is_remembering_obstacle):
            self.__car_action = "DRIVE_AROUND_OBSTACLE"
        else:
            self.__LineFollowService.follow_line_with_search()

        
    def drive_around_obstacle(self):
            print("Is on Line", self.__LineFollowService.is_on_line())
            if (self.__LineFollowService.is_on_line()):
                self.__car_action = "FOLLOW_LINE"
            else:
                self.__AvoidObstacleService.drive_around_obstacle()

    def update(self):
        self.__update_action()
        
        self.update_leds("OBSTACLE")

    def update_leds(self, display):
        if (display is None):
            return
        if display == "SEEING_OBSTACLE":
            self.set_pixels_seeing_obstacle()
        elif display == "AVOIDING_OBSTACLE":
            self.set_pixels_avoiding_obstacle()
        elif display == "LINE":
            self.set_pixels_line_following()
        
        self.__LedControl.pixels_show()
        
    def set_pixels_avoiding_obstacle(self):
        if (self.__AvoidObstacleService.avoiding_state == "SEARCHING"):
            self.__LedControl.pixels_fill(self.__LedControl.YELLOW)
        elif (self.__AvoidObstacleService.avoiding_state == "AVOIDING"):
            self.__LedControl.pixels_fill(self.__LedControl.RED)
        elif (self.__AvoidObstacleService.avoiding_state == "DRIVING"):
            self.__LedControl.pixels_fill(self.__LedControl.BLUE)
        
    def set_pixels_seeing_obstacle(self):
        if (self.__UltraSoundObstacleDetection.is_seeing_obstacle):
            self.__LedControl.pixels_fill(self.__LedControl.RED)
        else:
            self.__LedControl.pixels_fill(self.__LedControl.GREEN)
            
    def set_pixels_line_following(self):
        if (self.__LineFollowService.is_on_line()):
            self.__LedControl.pixels_fill(self.__LedControl.GREEN)
        else:
            self.__LedControl.pixels_fill(self.__LedControl.YELLOW)
        
    
