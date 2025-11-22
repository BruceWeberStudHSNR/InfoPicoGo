from Motor import MotorControl #importiert die Klasse MotorControl aus der Datei Motor.py
from TRSensor import TRSensor
from Ultrasonic_Ranging import dist
from machine import Pin
import time


# Initialisierung
IR_Sensor = TRSensor()
Motor = MotorControl() #legt ein neues Objekt names M der Klasse MotorControl an
Buzzer = Pin(4, Pin.OUT) #Buzzer zum aktivieren des Pieptons

IR_Sensor.calibrate()

obstacle_forget_time = 2000
obstacle_recognition_time = 3000
obstacle_recognition_start_time = 0
obstacle_recognition_distance = 20
obstacle_state = "NO_OBSTACLE" # / "OBSTACLE_IN_SIGHT" / "OBSTACLE_OUT_OF_SIGHT"

forward_speed = 50
turn_speed = 25
car_action = "FOLLOW_LINE" # / "AVOID_OBSTACLE" / "FIND_LINE" 

last_line_position = 0

while True:
    if (car_action == "FOLLOW_LINE"):
        # Check for Obstacles using Ultra Sound
        if (is_obstacle_detected(obstacle_recognition_distance)):
            current_time = time.ticks_ms()
            if (obstacle_state == "NO_OBSTACLE"):
                obstacle_state = "OBSTACLE_IN_SIGHT"
                obstacle_recognition_start_time = current_time
            elif (obstacle_state == "OBSTACLE_IN_SIGHT"):
                if current_time - obstacle_recognition_start_time >= obstacle_recognition_time:
                    car_action = "AVOID_OBSTACLE"
                    obstacle_recognition_start_time = 0
        else:
            # Fahre auf der Linie
            obstacle_state = "NO_OBSTACLE"
            position, line_sensore_values = IR_Sensor.readLine()
            if (line_sensore_values[0] + line_sensore_values[1] + line_sensore_values[2]+ line_sensore_values[3]+ line_sensore_values[4] > 4000):
                car_action = "RETURN_TO_LINE"

            else:
                motor_power_left, motor_power_right = line_position_to_motor_power(position, last_line_position, forward_speed)
                
                MotorControl.setMotor(motor_power_left,motor_power_right)

                last_line_position = position

    elif (car_action == "AVOID_OBSTACLE"):
        if obstacle_state == "OBSTACLE_IN_SIGHT":
            while (is_obstacle_detected(obstacle_recognition_distance)):
                MotorControl.right(turn_speed)
            obstacle_state = "OBSTACLE_OUT_OF_SIGHT"
            # turn right until no obstacle in sight
        if (obstacle_state == "OBSTACLE_OUT_OF_SIGHT"):
            # drive forward a bit
            MotorControl.forward(forward_speed)

            # turn left until obstacle in sight again
            #check for line
            position, line_sensore_values = IR_Sensor.readLine()
            if (line_sensore_values[0] + line_sensore_values[1] + line_sensore_values[2]+ line_sensore_values[3]+ line_sensore_values[4] > 4000):
                #line gefunden, FOLLOW_LINE
                last_line_position = position
                car_action = "FOLLOW_LINE"
                obstacle_state = "NO_OBSTACLE"

            # turn left until obstacle in sight again or searching for too long
            turn_start_time = time.ticks_ms()
            while (not is_obstacle_detected(obstacle_recognition_distance)):
                if (time.ticks_ms() - turn_start_time <= obstacle_forget_time): 
                    MotorControl.left(turn_speed)
                else:
                    car_action = "RETURN_TO_LINE"
                    break

            obstacle_state = "OBSTACLE_IN_SIGHT"
    elif (car_action == "RETURN_TO_LINE"):
        Buzzer.value(1) #Schreie bis du ausgeschaltet wirst
        # Fahre rum, vlt im zickzack
        # Wenn Linie erscheint car_action = FOLLOW_LINE

        # Wenn Obstacle erscheint switch auf AVOID_OBSTACLE
        if (is_obstacle_detected(obstacle_recognition_distance)):
            current_time = time.ticks_ms()
            if (obstacle_state == "NO_OBSTACLE"):
                obstacle_state = "OBSTACLE_IN_SIGHT"
                obstacle_recognition_start_time = current_time
            elif (obstacle_state == "OBSTACLE_IN_SIGHT"):
                if current_time - obstacle_recognition_start_time >= obstacle_recognition_time:
                    car_action = "AVOID_OBSTACLE"
                    obstacle_recognition_start_time = 0


#22.11.2025

