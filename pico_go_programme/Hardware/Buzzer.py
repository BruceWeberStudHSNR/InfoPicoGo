from machine import Pin

class Buzzer:
    def __init__(self):
        self.__BuzzerPin = Pin(4, Pin.OUT)

    def on(self):
        self.__BuzzerPin.value(1)

    def off(self):
        self.__BuzzerPin.value(0)
        
    def toggle(self):
        self.__BuzzerPin.value(not self.__BuzzerPin.value())
        
    def is_on(self):
        return self.__BuzzerPin.value() == 1
    
    def is_off(self):
        return self.__BuzzerPin.value() == 0