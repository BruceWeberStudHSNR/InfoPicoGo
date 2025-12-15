from TRSensor import TRSensor
from Motor import MotorControl
import time

#Beispiel Code um den PicoGo einer schwarzen Linie auf hellem Grund folgen zu lassen
#Zu Begin dreht sich der PicoGo, um sich zu kalibrieren


print("\nTRSensor Test Program ...\r\n")
time.sleep(3)
M = MotorControl()
TRS=TRSensor()
for i in range(100):
    if(i<25 or i>= 75):
        M.setMotor(30,-30)
    else:
        M.setMotor(-30,30)
    TRS.calibrate()
print("\ncalibrate done\r\n")
print(TRS.calibratedMin)
print(TRS.calibratedMax)
print("\ncalibrate done\r\n")
maximum = 30 #die Geschwindikeit mit der der Linie gefolgt werden soll
last_proportional = 0

while True:
    #print(TRS.readCalibrated())
    #print(TRS.readLine())
    position,Sensors = TRS.readLine()
    print(position)
    #time.sleep(0.1)
    if((Sensors[0] + Sensors[1] + Sensors[2]+ Sensors[3]+ Sensors[4]) > 4000):
        M.setMotor(0,0)
    else:
        # "proportional" ist 0, wenn der Roboter auf der Linie ist
        proportional = position - 2000

        derivative = proportional - last_proportional

        last_proportional = proportional
        
               
        
        power_difference = proportional/30  + derivative*2;  

        if (power_difference > maximum):
            power_difference = maximum
        if (power_difference < - maximum):
            power_difference = - maximum
        
        if (power_difference < 0):
            M.setMotor(maximum + power_difference, maximum)
        else:
            M.setMotor(maximum, maximum - power_difference)

