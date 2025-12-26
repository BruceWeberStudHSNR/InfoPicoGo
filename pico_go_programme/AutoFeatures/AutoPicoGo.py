from Hardware import MotorControl, TRSensor, UltraSoundSensor, LEDControl
from machine import Pin
from AutoFeatures import LineFollowService,AvoidObstacleService, UltraSoundObstacleDetection, PicoPilot
import utime


class AutoPicoGo():
    def __init__(self, 
                 forward_speed=20, 
                 turn_speed=15, 
                 is_checking_for_obstacles=True,
                 Motor=None,
                 Tr_sensor=None,
                 Led=None,
                 Ultra_sound=None,
                 Buzzer=None
    ):
        self.forward_speed = forward_speed
        self.turn_speed = turn_speed
        
        self.__car_action = "FOLLOW_LINE" #"FOLLOW_LINE" # / "DRIVE_AROUND_OBSTACLE" / "RETURN_TO_LINE" 
        self.is_checking_for_obstacles=is_checking_for_obstacles

        # Use passed Hardware classes or instantiate default
        self.__Motor = Motor if Motor is not None else MotorControl.MotorControl()
        self.__IRSensor = Tr_sensor if Tr_sensor is not None else TRSensor.TRSensor()
        self.__LedControl = Led if Led is not None else LEDControl.LEDControl()
        self.__USSensor = Ultra_sound if Ultra_sound is not None else UltraSoundSensor.UltraSoundSensor()

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
            time_service=self.__TimeService, 
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
        if (self.is_checking_for_obstacles):
            self.__UltraSoundObstacleDetection.detect_obstacle()
            
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
        self.update_leds("OBSTACLE")

    def update_leds(self, display):
        if (display is None):
            return
        if display == "SEEING_OBSTACLE":
            self.set_pixels_seeing_obstacle()
        elif display == "AVOIDING_OBSTACLE":
            self.set_pixels_avoiding_obstacle()
        # elif display == "LINE":         
        
        self.__LedControl.pixels_show()
        
    def set_pixels_avoiding_obstacle(self):
        if (self.__AvoidObstacleService.avoiding_state == "SEARCHING"):
            self.__LedControl.pixels_fill(self.__LedControl.BLUE)
        elif (self.__AvoidObstacleService.avoiding_state == "AVOIDING"):
            self.__LedControl.pixels_fill(self.__LedControl.RED)
        elif (self.__AvoidObstacleService.avoiding_state == "DRIVING"):
            self.__LedControl.pixels_fill(self.__LedControl.GREEN)
        
    def set_pixels_seeing_obstacle(self):
        if (self.__UltraSoundObstacleDetection.is_seeing_obstacle):
            self.__LedControl.pixels_fill(self.__LedControl.RED)
        else:
            self.__LedControl.pixels_fill(self.__LedControl.GREEN)
        
    
