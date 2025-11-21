

class LineFollowService():
    def __init__(self):
        self.__last_line_position = 0

    def line_position_to_motor_power(self,position, max_power):
        left = 0
        right = 0

        direction = position - 2000
        last_direction = self.__last_line_position - 2000

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
        
        self.__last_line_position = position

        return (left, right)