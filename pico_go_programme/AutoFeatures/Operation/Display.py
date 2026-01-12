import machine

class Display():

    # UI FINALS
    TRIGGER_DISTANCE_CM = 25      # Obstacle Avoidance Trigger Distance
    MAX_DISTANCE_CM = 80          # Max Distance to Display Obstacle

    # Car Position on Screen
    CAR_X = 120
    CAR_Y = 68

    # Line Display Configuration
    LINE_WIDTH = 6
    LINE_THICKNESS = 2


    def __init__(self, lcd, AvoidObstacleService, ObstacleDetection, LineDetection):
        self.__lcd = lcd
        self.__AvoidObstacleService = AvoidObstacleService
        self.__ObstacleDetection = ObstacleDetection
        self.__LineDetection = LineDetection

        # Battery Data
        self.__battery = machine.ADC(machine.Pin(26))

        # Ui Frames
        self.__ui_frame = 0


    # UI Functions
    #
    #  ______________________________
    # | Battery       Current State |
    # |             |               |
    # |            [ ]              |
    # |             |               |
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
        base_x, y = 50, 95
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
    def update(self):

        # Collect Data
        state = self.__AvoidObstacleService.avoiding_state
        distance = self.__ObstacleDetection.measured_distance * 10
        line_pos = self.__LineDetection.line_position

        v = self.__battery.read_u16() * 3.3 / 65535 * 2
        battery = max(0, min(100, (v - 3) * 100 / 1.2))

        # Fill Background
        bg = self.__lcd.BLACK
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