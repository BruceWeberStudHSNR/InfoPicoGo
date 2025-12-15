import utime
from machine import Pin

class UltraSoundSensor():

    def __init__(self, pin_in, pin_out):
        self.__self.__echo = Pin(pin_out, Pin.IN)
        self.__self.__trig = Pin(pin_in, Pin.OUT)
        self.__self.__trig.value(0)
        self.__self.__echo.value(0)

    def get_distance(self):
        self.__trig.value(1)
        utime.sleep_us(10)
        self.__trig.value(0)
        while(self.__echo.value() == 0):
            pass
        ts=utime.ticks_us()
        while(self.__echo.value() == 1):
            pass
        te=utime.ticks_us()
        distance=((te-ts)*0.034)/2
        return distance
