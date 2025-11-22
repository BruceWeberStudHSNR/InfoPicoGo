

import time

from Info.pico_go_programme.Motor import MotorControl
from Info.pico_go_programme.TRSensor import TRSensor


class LineFollowService():
    def __init__(self, IRSensor=None, Motor=None, forward_speed=0, time_service=None, dash_time=2000, turn_time=1000):
        # compatible constructor: (IRSensor, Motor, forward_speed)
        self.__IRSensor = IRSensor if IRSensor is not None else TRSensor()
        self.__Motor = Motor if Motor is not None else MotorControl()
        self.__time_service = time_service if time_service is not None else time
        
        self.__last_line_position = 0
        self.forward_speed = forward_speed
        self.__line_state = "SEARCHING" # "SEARCHING" or "ON_LINE"
        
        # Parameters for searching behaviour (maybe own class later)
        self.__searching_dash_time = dash_time
        self.__searching_turn_time = turn_time
        self.__searching_timer = 0
        self.__searching_state = "DASHING" # "DASHING" or "TURNING"
        
    def follow_line_with_search(self):
        position, line_sensore_values = self.__IRSensor.readLine()
        
        if (self.__sees_line(line_sensore_values)):
            self.drive_along_line(position, self.__last_line_position)
        else:
            self.search_for_line()
            
        self.__last_line_position = position
            
    def search_for_line(self):
        current_time = self.__time_service.ticks_ms()
        if (self.__line_state != "SEARCHING"):
            self.__searching_timer = current_time
            
        self.__line_state = "SEARCHING" # "SEARCHING" or "ON_LINE"
        
        # Alternate between dashing forward and turning right to find the line
        if (self.__searching_state == "DASHING"):
            if (current_time - self.__searching_timer) < self.__searching_dash_time:
                self.__Motor.forward(self.forward_speed)
            else:
                self.__searching_state = "TURNING"
                self.__searching_timer = current_time
        elif (self.__searching_state == "TURNING"):
            if (current_time - self.__searching_timer) < self.__searching_turn_time:
                self.__Motor.right(self.forward_speed)
            else:
                self.__searching_state = "DASHING"
                self.__searching_timer = current_time


    def get_line_state(self):
        return self.__line_state
    
    def __sees_line(self,line_sensore_values):
        return line_sensore_values[0] + line_sensore_values[1] + line_sensore_values[2]+ line_sensore_values[3]+ line_sensore_values[4] < 4000
    
    def drive_along_line(self, position, last_position):
        self.__line_state = "ON_LINE"
        motor_power_left, motor_power_right = self.__calculate_motor_power(position, last_position, self.forward_speed)
        self.__Motor.setMotor(motor_power_left,motor_power_right)


    def __calculate_motor_power(self,position, last_position, max_power):
        left = 0
        right = 0

        direction = position - 2000
        last_direction = last_position - 2000

        change_in_direction = direction - last_direction

        power_difference = direction/30  + change_in_direction*2;  

        if (power_difference > max_power):
            power_difference = max_power
        if (power_difference < - max_power):
            power_difference = - max_power

        if (power_difference < 0):
            left,right = (max_power + power_difference, max_power)
        else:
            left,right = (max_power, max_power - power_difference)

        return (left, right)