
class LightOperator():
    def __init__(self,Led, Colors=None):
        self.__LedControl = Led
        self.colors = Colors if Colors is not None else Default_Colors()
        
    def set_lights_fill(self,color):
        self.__LedControl.pixels_fill(color)
        
    def update_leds(self, led_mode, avoiding_state, is_remembering_obstacle, is_on_line):
        if led_mode == "SEEING_OBSTACLE":
            self.set_pixels_seeing_obstacle(is_remembering_obstacle)
        elif led_mode == "AVOIDING_OBSTACLE":
            self.set_pixels_avoiding_obstacle(avoiding_state)
        elif led_mode  == "LINE":
            self.set_pixels_line_following(is_on_line)
        elif led_mode  == "avoid_with_seeing":
            self.avoid_with_obstacle(avoiding_state, is_remembering_obstacle)
        elif led_mode  == "LINE_AND_OBSTACLE":
            if is_remembering_obstacle:
                self.avoid_with_obstacle(is_remembering_obstacle)
            else:
                self.set_pixels_follow_line_mode(is_on_line)

        self.__LedControl.pixels_show()
        
    def set_pixels_avoiding_obstacle(self, avoiding_state):
        if (avoiding_state == "SEARCHING"):
            self.__LedControl.pixels_fill(self.colors.GREEN)
        elif (avoiding_state == "AVOIDING"):
            self.__LedControl.pixels_fill(self.colors.CYAN)
        elif (avoiding_state == "DRIVING"):
            self.__LedControl.pixels_fill(self.colors.BLUE)

    def avoid_with_obstacle(self,avoiding_state, is_seeing_obstacle):
        self.set_pixels_avoiding_obstacle(avoiding_state)

        if (is_seeing_obstacle):
            self.__LedControl.pixels_set(0, self.colors.RED)
            self.__LedControl.pixels_set(1, self.colors.RED)
        else:
            self.__LedControl.pixels_set(0, self.colors.YELLOW)
            self.__LedControl.pixels_set(1, self.colors.YELLOW)
            
    def set_pixels_follow_line_mode(self, obstacle_detected):
        if (obstacle_detected):
            self.__LedControl.pixels_fill(self.colors.RED)
        else:
            self.__LedControl.pixels_fill(self.colors.GREEN)
        
    def set_pixels_seeing_obstacle(self, is_remembering_obstacle):
        if (is_remembering_obstacle):
            self.__LedControl.pixels_fill(self.colors.RED)
        else:
            self.__LedControl.pixels_fill(self.colors.GREEN)
            
    def set_pixels_line_following(self,is_on_line):
        if (is_on_line):
            self.__LedControl.pixels_fill(self.colors.GREEN)
        else:
            self.__LedControl.pixels_fill(self.colors.YELLOW)
        
class Default_Colors():
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 150, 0)
        self.GREEN = (0, 255, 0)
        self.CYAN = (0, 255, 255)
        self.BLUE = (0, 0, 255)
        self.PURPLE = (180, 0, 255)
        self.WHITE = (255, 255, 255)
        self.COLORS = (self.BLACK, self.RED, self.YELLOW, self.GREEN, self.CYAN, self.BLUE, self.PURPLE, self.WHITE)
        