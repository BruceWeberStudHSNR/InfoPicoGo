import utime
from machine import Pin
from Motor import MotorControl

#Weicht Hindernissen mittles Ultraschallsensor aus und den beiden Infrarotsensoren vorne aus
#Ist quasi eine Kombination der Demos Ultrasonic_obstacle_Avoidance.py und Infrared_obstacle_Avoidance.py
#Wenn einer der Infrarotsensoren etwas sieht, oder die Entfernung des Ultraschallsensors kleinergleich 20 ist wird nach rechts gedreht
#Ansonsten geradeaus

M = MotorControl()
DSR = Pin(2, Pin.IN)
DSL = Pin(3, Pin.IN)
Echo = Pin(15, Pin.IN)
Trig = Pin(14, Pin.OUT)
Trig.value(0)
Echo.value(0)


#Misst die Entfernung mittels Ultraschallsensor und gibt die Entfernung in cm zurück
#Hinweis: exakt die gleiche Methode wie in Ultrasonic_Ranging.py
def dist():
    Trig.value(1)
    utime.sleep_us(10)
    Trig.value(0)
    while(Echo.value() == 0):
        pass
    ts=utime.ticks_us()
    while(Echo.value() == 1):
        pass
    te=utime.ticks_us()
    distance=((te-ts)*0.034)/2
    return distance

while True:
    D = dist()
    DR_status = DSR.value()
    DL_status = DSL.value()
    if((D <= 20) or (DL_status == 0) or (DR_status == 0)):
        M.right(20)
        #Ab.left()
    else:
        M.forward(40)
        
    utime.sleep_ms(20)
