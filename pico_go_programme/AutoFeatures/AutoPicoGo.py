from machine import Pin

class AutoPicoGo():
    def __init__(self,
                Motor,
                Tr_sensor,
                Led,
                Ultra_sound,
                Buzzer,
                TimeService,
                Pilot,
                LightOperator,
                LineDetection,
                LineFollowing,
                ObstacleDetection,
                ObstacleAversion,
                forward_speed=20,
                speed_levels=[20, 40, 60, 80, 100],
                turn_speed=15, 
                is_checking_for_obstacles=True,
                led_mode="AVOIDING_OBSTACLE",
    ):
        self.forward_speed = forward_speed
        self.turn_speed = turn_speed
        self.__led_mode = led_mode
        
        self.__car_action = "FOLLOW_LINE" #"FOLLOW_LINE" # / "DRIVE_AROUND_OBSTACLE" 
        self.is_checking_for_obstacles=is_checking_for_obstacles

        self.__timer = 0

        # Use passed Hardware classes or instantiate default
        self.__Motor = Motor 
        self.__IRSensor = Tr_sensor 
        self.__LedControl = Led
        self.__USSensor = Ultra_sound
        self.__Buzzer = Buzzer 
        self.__TimeService = TimeService

        self.__Pilot = Pilot

        self.__LightOperator = LightOperator
        # --- 2) instantiate services, passing hardware instances ---

        self.__LineDetection = LineDetection
        self.__LineFollowService = LineFollowing
        self.__ObstacleDetection = ObstacleDetection      
        self.__AvoidObstacleService = ObstacleAversion


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
            self.__ObstacleDetection.detect_obstacle()

        self.__LineDetection.detect_line()
            
    def act(self):
        if(self.__car_action == "FOLLOW_LINE"):
            self.follow_line()
        elif(self.__car_action == "DRIVE_AROUND_OBSTACLE"):
            self.drive_around_obstacle()

    def follow_line(self):        
        if (self.__ObstacleDetection.is_recognising_obstacle):
            self.__car_action = "DRIVE_AROUND_OBSTACLE"
        else:
            self.__LineFollowService.follow_line()

    def drive_around_obstacle(self):
        self.__AvoidObstacleService.drive_around_obstacle()

        if (self.__LineDetection.is_on_line and not self.__ObstacleDetection.is_seeing_obstacle):
            # Might cause problems because it cannot leave the line to avoid an obstacle
            self.__car_action = "FOLLOW_LINE"
            self.__ObstacleDetection.is_remembering_obstacle = False

    def update_ui(self):
        self.__LightOperator.update_leds(
            self.__led_mode, 
            self.__AvoidObstacleService.avoiding_state, 
            self.__ObstacleDetection.is_remembering_obstacle, 
            is_on_line=self.__LineDetection.is_on_line)
        
        self.update_buzzer()
        
        # TODO: update screen
        
    def update_buzzer(self):
        if (self.__ObstacleDetection.is_seeing_obstacle):
            self.__Buzzer.buzz_on()
        else:
            self.__Buzzer.buzz_off()

        
    
