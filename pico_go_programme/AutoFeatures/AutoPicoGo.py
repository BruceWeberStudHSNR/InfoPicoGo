from machine import Pin

class AutoPicoGo():

    # UI FINALS
    TRIGGER_DISTANCE_CM = 25      # Obstacle Avoidance Trigger Distance
    MAX_DISTANCE_CM = 80          # Max Distance to Display Obstacle

    # Car Position on Screen
    CAR_X = 120
    CAR_Y = 70

    # Line Display Configuration
    LINE_WIDTH = 6
    LINE_THICKNESS = 2

    def __init__(self,
                 Motor,
                 Tr_sensor,
                 Led,
                 Ultra_sound,
                 Buzzer,
                 lcd,
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
        self.__car_action = "FOLLOW_LINE" #"FOLLOW_LINE" # / "DRIVE_AROUND_OBSTACLE" / "RETURN_TO_LINE" 
        self.is_checking_for_obstacles=is_checking_for_obstacles

        # Use passed Hardware classes or instantiate default
        self.__Motor = Motor 
        self.__IRSensor = Tr_sensor 
        self.__LedControl = Led
        self.__USSensor = Ultra_sound
        self.__Buzzer = Buzzer 
        self.__lcd = lcd
        self.__TimeService = TimeService
        self.__Pilot = Pilot
        self.__LightOperator = LightOperator
        self.__LineDetection = LineDetection
        self.__LineFollowService = LineFollowing
        self.__ObstacleDetection = ObstacleDetection      
        self.__AvoidObstacleService = ObstacleAversion
        # self.__Buzzer = buzzer if buzzer is not None else Buzzer.Buzzer()
        # --- 2) instantiate services, passing hardware instances ---

        # Battery Data
        self.__battery = machine.ADC(Pin(26))

        # Ui Frames
        self.__ui_frame = 0


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
        if (self.__LineDetection.is_on_line):
            # Might cause problems because it cannot leave the line to avoid an obstacle
            self.__car_action = "FOLLOW_LINE"
        else:
            self.__AvoidObstacleService.drive_around_obstacle()

    # Update Buzzer -> Buzzing when Obstacle is detected
    def update_buzzer(self):
        if (self.__ObstacleDetection.is_recognising_obstacle):
            self.__Buzzer.buzz_on()
        else:
            self.__Buzzer.buzz_off()




    # UI Functions
    #
    #  ______________________________
    # | Battery       Current State |
    # |                             |
    # | ------------[][]----------- |
    # |                             |
    # | US Dist       Line Position |
    # |_____________________________|

    # Display Ultrasonic Distance to Obstacle with Trigger Line    
    def _draw_ultrasonic(self, distance):
        x, y = 150, 90
        width, height = 70, 8

        self.__lcd.text("DIST", x, y - 12, self.__lcd.WHITE)
        self.__lcd.rect(x, y, width, height, self.__lcd.WHITE)

        if distance is None or distance <= 0:
            self.__lcd.text("--cm", x, y + 12, self.__lcd.WHITE)
            return

        d = min(distance, self.MAX_DISTANCE_CM)
        fill = int((self.MAX_DISTANCE_CM - d) / self.MAX_DISTANCE_CM * width)

        # Change Color and Animation depending on Distance
        if d < 15:
            color = self.__lcd.ORANGE if self.__ui_frame % 10 < 5 else self.__lcd.BLACK
        elif d < 30:
            color = self.__lcd.PURPLE
        elif d < 60:
            color = self.__lcd.GREEN
        else:
            color = self.__lcd.WHITE

        self.__lcd.fill_rect(x, y, fill, height, color)

        # Trigger Line
        trigger_x = int(
            x + (self.MAX_DISTANCE_CM - self.TRIGGER_DISTANCE_CM)
            / self.MAX_DISTANCE_CM * width
        )
        self.__lcd.line(trigger_x, y - 2, trigger_x, y + height + 2, self.__lcd.ORANGE)

        self.__lcd.text(f"{int(d)}cm", x, y + 12, self.__lcd.WHITE)

    # Display Line Position as Boxes example: [x] [] [] -> Line is on the left
    def _draw_line_position(self, pos):
        base_x, y = 80, 95
        self.__lcd.text("LINE", base_x - 15, y - 12, self.__lcd.WHITE)

        self.__lcd.rect(base_x - 30, y, 10, 10, self.__lcd.WHITE)
        self.__lcd.rect(base_x, y, 10, 10, self.__lcd.WHITE)
        self.__lcd.rect(base_x + 30, y, 10, 10, self.__lcd.WHITE)

        if pos < 0:
            self.__lcd.fill_rect(base_x - 30, y, 10, 10, self.__lcd.GREEN)
        elif pos == 0:
            self.__lcd.fill_rect(base_x, y, 10, 10, self.__lcd.GREEN)
        elif pos > 0:
            self.__lcd.fill_rect(base_x + 30, y, 10, 10, self.__lcd.GREEN)

    # Display Car as Rectangle 
    def _draw_car_topdown(self):
        self.__lcd.fill_rect(
            self.CAR_X - 10,
            self.CAR_Y - 15,
            20,
            30,
            self.__lcd.WHITE
        )

    # Display Line relative to Car
    def _draw_line_topdown(self, line_pos):

        offset = 0

        if line_pos < 0:
            offset = -20
        elif line_pos > 0:
            offset = 20

        line_x = self.CAR_X + offset - self.LINE_WIDTH // 2

        for i in range(self.LINE_THICKNESS):
            self.__lcd.vline(
                line_x + i,
                0,
                135,
                self.__lcd.WHITE
            )

    # Update the LED, Buzzer and Display
    def update_ui(self):

        # Update LED
        self.__LightOperator.update_leds(
            self.__led_mode,
            self.__AvoidObstacleService.avoiding_state,
            self.__ObstacleDetection.is_remembering_obstacle,
            is_on_line=self.__LineDetection.is_on_line
        )

        # Update Buzzer
        self.update_buzzer()

        # Collect Data
        state = self.__AvoidObstacleService.avoiding_state
        distance = self.__USSensor.get_distance()
        line_pos = self.__LineDetection.line_position

        v = self.__battery.read_u16() * 3.3 / 65535 * 2
        battery = max(0, min(100, (v - 3) * 100 / 1.2))

        # Fill Background
        bg = self.__lcd.BLACK if self.ui_mode == self.UI_MINIMAL else self.__lcd.DARKBLUE
        self.__lcd.fill(bg)

        # Draw Line
        self._draw_line_topdown(line_pos=line_pos)

        # Draw Car
        self._draw_car_topdown()

        # Draw State
        color = self.__lcd.ORANGE
        if state == "DRIVING":
            color = self.__lcd.GREEN
        elif state == "AVOIDING":
            color = self.__lcd.PURPLE

        self.__lcd.text(state, 5, 5, color)
        self.__lcd.text(f"{int(battery)}%", 185, 5, self.__lcd.WHITE)

        # Draw Line Position
        self._draw_line_position(line_pos)

        # Draw Ultrasonic Distance
        self._draw_ultrasonic(distance)

        # Update Display
        self.__lcd.show()
        self.__ui_frame += 1


        
    
# TODO: LineDetection.line_position Check Return Values for LEFT RIGHT CENTER for _draw_line_position and _draw_line_topdown
# TODO: Ultra_sound.get_distance() return cm or None Check
# TODO: Check if Layout is correct
# TODO: Check if Finals are necesarry
# TODO: Comment