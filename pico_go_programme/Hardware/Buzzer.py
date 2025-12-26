from machine import Pin

class Buzzer ():
    def __init__ (self):
        self.buzzer_pin = Pin(15, Pin.OUT)

    def buzz_on(self):
        self.buzzer_pin.value(1)

    def buzz_off(self):
        self.buzzer_pin.value(0)