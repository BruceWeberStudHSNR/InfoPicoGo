from Info.pico_go_programme.AutoFeatures import ObstacleDetection
from machine import Pin
from AutoFeatures import LineFollowService,AvoidObstacleService, PicoPilot,LineDetection,LightOperator

class AutoPicoGo():
    def __init__(self,
                 Motor,
                 Tr_sensor,
                 Led,
                 Ultra_sound,
                 Buzzer,
                 TimeService,
                 forward_speed=20, 
                 turn_speed=15, 
                 is_checking_for_obstacles=True,
                 led_mode="AVOIDING_OBSTACLE",
    ):
        self.forward_speed = forward_speed
        self.turn_speed = turn_speed
        self.__led_mode = led_mode
        
        self.__car_action = "FOLLOW_LINE" #"FOLLOW_LINE" # / "DRIVE_AROUND_OBSTACLE" / "RETURN_TO_LINE" 
        self.is_checking_for_obstacles=is_checking_for_obstacles

        # Use passed Hardware classes or instantiate default
        self.__Motor = Motor 
        self.__IRSensor = Tr_sensor 
        self.__LedControl = Led
        self.__USSensor = Ultra_sound
        self.__Buzzer = Buzzer 
        self.__TimeService = TimeService

        self.__Pilot = PicoPilot.PicoPilot(
            Motor=self.__Motor,
            TimeService=self.__TimeService
        )
        
        self.__LightOperator = LightOperator.LightOperator(
            Led=self.__LedControl            )
        # self.__Buzzer = buzzer if buzzer is not None else Buzzer.Buzzer()
        # --- 2) instantiate services, passing hardware instances ---

        self.__LineDetection = LineDetection.LineDetection(
            TRSensor=self.__IRSensor,
            TimeService=self.__TimeService,
            on_line_threshold=2000,
            forget_line_time=1000,
            recognize_line_time=100
        )
        self.__LineFollowService = LineFollowService.LineFollowService(
            Pilot=self.__Pilot,
            LineDetection=self.__LineDetection,
            dash_time=2000, 
            turn_time=1000)
        self.__UltraSoundObstacleDetection = ObstacleDetection.ObstacleDetection(
            self.__USSensor, 
            self.__TimeService)        
        self.__AvoidObstacleService = AvoidObstacleService.AvoidObstacleService(
            self.__TimeService, 
            self.__Motor, 
            self.__LedControl, 
            self.__UltraSoundObstacleDetection )


    def run(self):
        self.scan()

        self.act()

        self.update_ui()


    def calibrate_line_sensors(self):
        print("Calibrate Start")
        self.__LedControl.pixels_fill(self.__LedControl.PURPLE)
        self.__LedControl.pixels_show()
        for i in range(100):
            if(i<25 or i>= 75):
                self.__Pilot.left(30)
            else:
                self.__Pilot.right(30)
            self.__IRSensor.calibrate()

        print ("Calibrate End")

    def scan(self):
        if(self.is_checking_for_obstacles):
            self.__UltraSoundObstacleDetection.detect_obstacle()

        self.__LineDetection.detect_line()
            
    def act(self):
        if(self.__car_action == "FOLLOW_LINE"):
            self.follow_line()
        elif(self.__car_action == "DRIVE_AROUND_OBSTACLE"):
            self.drive_around_obstacle()

    def follow_line(self):        
        if (self.__UltraSoundObstacleDetection.is_remembering_obstacle):
            self.__car_action = "DRIVE_AROUND_OBSTACLE"
        else:
            self.__LineFollowService.follow_line()

    def drive_around_obstacle(self):
        if (self.__LineDetection.is_on_line):
            self.__car_action = "FOLLOW_LINE"
        else:
            self.__AvoidObstacleService.drive_around_obstacle()

    def update_ui(self):
        self.__LightOperator.update_leds(
            self.__led_mode, 
            self.__AvoidObstacleService.avoiding_state, 
            self.__UltraSoundObstacleDetection.is_remembering_obstacle, 
            is_on_line=self.__LineDetection.is_on_line)
        
        #self.update_buzzer()

        
    
