import array, time
from machine import Pin
import rp2

#Bietet Methoden um die 4 LEDs unten am PicoGo anzusteuern
#Kann in andere Klassen importiert werden
#Ganz unten finden Sie ein Beispiel


NUM_LEDS = 4
PIN_NUM = 22

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()
    
    
#Initialisierung der LED_Steuerung (wird beim Erstellen ausgeführt)       
class LEDControl(object):
    def __init__(self,pin=PIN_NUM,num=NUM_LEDS,brightness=0.8):
        self.pin=pin
        self.num=num
        self.brightness = brightness
        
        self.sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

        self.sm.active(1)

        self.ar = array.array("I", [0 for _ in range(self.num)])
        
        
        #Vordefinierte Farben
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 150, 0)
        self.GREEN = (0, 255, 0)
        self.CYAN = (0, 255, 255)
        self.BLUE = (0, 0, 255)
        self.PURPLE = (180, 0, 255)
        self.WHITE = (255, 255, 255)
        self.COLORS = (self.BLACK, self.RED, self.YELLOW, self.GREEN, self.CYAN, self.BLUE, self.PURPLE, self.WHITE)
        
    ##########################################################################
    #diese Methode aktiviert die LEDs in der mit anderen Methoden gewählten Farben
    #Muss nach den Methoden pixels_set, pixels_fill ausgeführt werden um diese anzuwenden
    def pixels_show(self):
        dimmer_ar = array.array("I", [0 for _ in range(self.num)])
        for i,c in enumerate(self.ar):
            r = int(((c >> 8) & 0xFF) * self.brightness)
            g = int(((c >> 16) & 0xFF) * self.brightness)
            b = int((c & 0xFF) * self.brightness)
            dimmer_ar[i] = (g<<16) + (r<<8) + b
        self.sm.put(dimmer_ar, 8)
    
    
    #setzt eine LED auf die gewählte Farbe
    #entweder eine der vordefinierten Farben oben übergeben
    # oder die Farbe in RGB Werten (x,y,z)
    #i gibt die geählte LED an
    def pixels_set(self, i, color):
        self.ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

    #setzt alle LEDs auf die gewählte Farbe
    #entweder eine der vordefinierten Farben oben übergeben
    # oder die Farbe in RGB Werten (x,y,z)
    def pixels_fill(self, color):
        for i in range(len(self.ar)):
            self.pixels_set(i, color)

    #setzt alle LEDs einer nach der anderen auf die gewählte Farbe
    #wait definiert wie viel Zeit zwischen dem Wechsel der einzelnen LEDs liegt
    def color_chase(self, color, wait):
        for i in range(self.num):
            self.pixels_set(i, color)
            time.sleep(wait)
            self.pixels_show()
        time.sleep(0.2)
     
    #Man übergibt eine Zahl zwischen 0 und 255, um einen Farbwert zurückzubekommen
    #Die Farben gehten stufenweise von Rot zu Grün zu Blau zu Schwarz und wieder zu Rot
    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)
     
    #Nutzt die Methode wheel und pixels_set, um jede LED einzeln einen Regenbogen durchlaufen zu lassen
    #Wait definiert die zeit zwischen den Farben
    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.num):
                rc_index = (i * 256 // self.num) + j
                self.pixels_set(i, self.wheel(rc_index & 255))
            self.pixels_show()
            time.sleep(wait)

if __name__=='__main__':
    #Beispielanwendung
    strip = LEDControl()
    
    strip.pixels_fill(strip.GREEN) #setze alle LEDs auf Grün
    strip.pixels_show()
    
    time.sleep(2) #warte 2 Sekunde
    
    strip.pixels_set(1, strip.RED) #setze LED 1 auf Rot
    strip.pixels_set(3, (0, 0, 255)) #setze LED 3 auf Blau (Blau hier in RGB Wert angegeben)
    strip.pixels_show()
    
    time.sleep(2) #warte 2 Sekunde
    
    strip.color_chase(strip.PURPLE, 1) # setzt die LEDs nacheinander auf violett, mit 1 Sekunde zwischen den LEDs

    time.sleep(1) #warte 2 Sekunde

    strip.rainbow_cycle(0.02) #starte den Regenbogen Effekt

