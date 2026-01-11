
class LineDetection:
    # TRSensor Interface
    # readLine() -> (number, Array<number>)
    
    # TimeService Interface
    # ticks_ms() -> number    
    def __init__(self, TRSensor, TimeService, on_line_threshold=2000, recognize_line_time=50, forget_line_time=200):
        self.__TRSensor = TRSensor
        self.__TimeService = TimeService
        self.__on_line_threshold = on_line_threshold
        self.__recognize_line_time = recognize_line_time
        self.__time_counter = self.__TimeService.ticks_ms()
        self.__forget_line_time = forget_line_time
        
        self.is_on_line = False
        self.is_recognizing_line = False
        
        self.line_position = 0
        self.last_line_position = 0
        self.line_sensor_values = []
        
    def __update_on_line_state(self, new_is_on_line, current_time):
        if (self.is_on_line != new_is_on_line):
            #print("Line state changed to:", new_is_on_line)
            self.__time_counter = current_time
            self.is_on_line = new_is_on_line
            
    def __update_recognizing_line_state(self, on_line, current_time, threshhold):
        if (self.__TimeService.has_time_elapsed(self.__time_counter, threshhold)):
            self.__time_counter = current_time
            self.is_recognizing_line = on_line
        
    def detect_line(self):
        position, line_sensore_values = self.__TRSensor.readLine() # Read Sesnor input
        current_time = self.__TimeService.ticks_ms()
        is_on_line = self.is_line_visible(line_sensore_values)

        self.__update_on_line_state(is_on_line, current_time)
        
        self.__update_recognizing_line_state(
            is_on_line, 
            current_time, 
            self.__recognize_line_time if is_on_line else self.__forget_line_time
            )
        self.last_line_position = self.line_position
        self.line_position = position
        self.line_sensor_values = line_sensore_values
        
        return (position, line_sensore_values) 
    
    def is_line_visible(self,line_sensore_values):
        average_value = sum(line_sensore_values) / len(line_sensore_values)
        return average_value < self.__on_line_threshold
#Kommentar