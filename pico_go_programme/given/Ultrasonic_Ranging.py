import utime
from machine import Pin

#Demo für eine Entfernungsmessung mittels des Ultraschallsensors
#Misst einmal pro Sekunde und gibt denn gemessenen Wert in cm aus

Echo = Pin(15, Pin.IN)
Trig = Pin(14, Pin.OUT)
Trig.value(0)
Echo.value(0)

#Misst die Entfernung mittels Ultraschallsensor und gibt die Entfernung in cm zurück
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
    print("Distance:%6.2f cm" % dist())
    utime.sleep(1)