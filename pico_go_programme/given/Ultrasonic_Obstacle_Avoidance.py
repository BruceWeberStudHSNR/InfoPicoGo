import utime
from machine import Pin
from Motor import MotorControl

#Weicht Hindernissen mittles Ultraschallsensor aus
#Fährt immer vorwärts, es sei denn ein Hinderniss ist 20cm oder näher
#Wenn ein Hinderniss näher ist, dreht sich der PicoGo nach links


M = MotorControl()
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
    if(D <= 20):
        M.right(20)
        #Ab.left()
    else:
        M.forward(20)
        
    utime.sleep_ms(20)
