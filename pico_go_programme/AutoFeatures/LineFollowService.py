from Helper.has_time_elapsed import has_time_elapsed

class LineFollowService():
    def __init__(self, 
                 Pilot, 
                 LineDetection,
                 dash_time=2000, 
                 turn_time=1000):
        self.__Pilot = Pilot
        self.__LineDetection = LineDetection
        
        # Parameters for searching behaviour (maybe own class later)
        self.__searching_dash_time = dash_time
        self.__searching_turn_time = turn_time
        self.searching_state = "DASHING" # "DASHING" or "TURNING"
        
    def follow_line(self):        
        if (self.__LineDetection.is_recognizing_line):
            self.drive_along_line(self.__LineDetection.line_position, self.__LineDetection.last_line_position)
            
        else:
            self.search_for_line()
                
    def search_for_line(self):        
        # Alternate between dashing forward and turning right to find the line
        if (self.searching_state == "DASHING"):
            self.__Pilot.go_direction_for_ms("FORWARD", self.__searching_dash_time, speed=self.__Pilot.default_speed/2)
            self.__update_searching_state("TURNING")

        elif (self.searching_state == "TURNING"):
            self.__Pilot.go_direction_for_ms("RIGHT", self.__searching_turn_time, speed=self.__Pilot.default_speed/2)
            self.__update_searching_state("DASHING")
    
    def drive_along_line(self, position, last_position):
        motor_power_left, motor_power_right = self.__calculate_motor_power_to_line(position, last_position,self.__Pilot.default_speed)
        self.__Pilot.set_wheels(motor_power_left,motor_power_right)

    def __update_searching_state(self, new_state):
        if (self.__Pilot.has_stopped):
            self.searching_state = new_state
            

    def __calculate_motor_power_to_line(self,position, last_position, max_power):
        left = 0
        right = 0
        
        correction_factor = 30 # Higher = More aggressive turning towards line
        inertia = 2      # Higher = More smoothing of direction changes

        direction = position - 2000
        last_direction = last_position - 2000

        change_in_direction = direction - last_direction

        power_difference = direction/correction_factor  + change_in_direction*inertia;  

        if (power_difference > max_power):
            power_difference = max_power
        if (power_difference < - max_power):
            power_difference = - max_power

        if (power_difference < 0):
            left,right = (max_power + power_difference, max_power)
        else:
            left,right = (max_power, max_power - power_difference)

        return (left, right)