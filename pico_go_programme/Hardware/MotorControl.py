from machine import Pin, PWM
import time

#Bietet Methoden zur Motorsteuereung des PicoGo

class MotorControl(object):
    #Initialisierung der Motorsteuerung (wird beim Erstellen ausgeführt)
    def __init__(self):
        print("init motor")
        self.PWMA = PWM(Pin(16))
        self.PWMA.freq(1000)
        self.AIN2 = Pin(17, Pin.OUT)
        self.AIN1 = Pin(18, Pin.OUT)
        self.BIN1 = Pin(19, Pin.OUT)
        self.BIN2 = Pin(20, Pin.OUT)
        self.PWMB = PWM(Pin(21))
        self.PWMB.freq(1000)
        self.stop()
    
    #vorwärts fahren
    #speed: die Geschwindigkeit in Prozent (0 bis 100) 
    def forward(self,speed):
        if((speed >= 0) and (speed <= 100)):
            self.PWMA.duty_u16(int(speed*0xFFFF/100))
            self.PWMB.duty_u16(int(speed*0xFFFF/100))
            self.AIN2.value(1)
            self.AIN1.value(0)
            self.BIN2.value(1)
            self.BIN1.value(0)
      
    #rückwärts fahren
    #speed: die Geschwindigkeit in Prozent (0 bis 100)
    def backward(self,speed): 
        if((speed >= 0) and (speed <= 100)):
            self.PWMA.duty_u16(int(speed*0xFFFF/100))
            self.PWMB.duty_u16(int(speed*0xFFFF/100))
            self.AIN2.value(0)
            self.AIN1.value(1)
            self.BIN2.value(0)
            self.BIN1.value(1)
    
    #nach links drehen (auf der Stelle)
    #speed: die Geschwindigkeit in Prozent (0 bis 100)
    def left(self,speed):
        
        if((speed >= 0) and (speed <= 100)):
            self.PWMA.duty_u16(int(speed*0xFFFF/100))
            self.PWMB.duty_u16(int(speed*0xFFFF/100))
            self.AIN2.value(0)
            self.AIN1.value(1)
            self.BIN2.value(1)
            self.BIN1.value(0)
    
    #nach rechts drehen (auf der Stelle)
    #speed: die Geschwindigkeit in Prozent (0 bis 100)
    def right(self,speed):
        if((speed >= 0) and (speed <= 100)):
            self.PWMA.duty_u16(int(speed*0xFFFF/100))
            self.PWMB.duty_u16(int(speed*0xFFFF/100))
            self.AIN2.value(1)
            self.AIN1.value(0)
            self.BIN2.value(0)
            self.BIN1.value(1)
            
    #stoppt beide Motoren
    def stop(self):
        self.PWMA.duty_u16(0)
        self.PWMB.duty_u16(0)
        self.AIN2.value(0)
        self.AIN1.value(0)
        self.BIN2.value(0)
        self.BIN1.value(0)
    
    #Steuert die beiden Motoren einzeln an (z.B. für Kurven)
    #left: Geschwindikeit des linken Motors in Prozent. Negative Zahlen für rückwärts  (d.h. Werte von -100 bis 100)#
    #right: Geschwindikeit des rechten Motors in Prozent. Negative Zahlen für rückwärts  (d.h. Werte von -100 bis 100)
    def setMotor(self, left, right):
        if((left >= 0) and (left <= 100)):
            self.AIN1.value(0)
            self.AIN2.value(1)
            self.PWMA.duty_u16(int(left*0xFFFF/100))
        elif((left < 0) and (left >= -100)):
            self.AIN1.value(1)
            self.AIN2.value(0)
            self.PWMA.duty_u16(-int(left*0xFFFF/100))
        if((right >= 0) and (right <= 100)):
            self.BIN2.value(1)
            self.BIN1.value(0)
            self.PWMB.duty_u16(int(right*0xFFFF/100))
        elif((right < 0) and (right >= -100)):
            self.BIN2.value(0)
            self.BIN1.value(1)
            self.PWMB.duty_u16(-int(right*0xFFFF/100))

if __name__=='__main__':
    import utime
    #Beispielcode zum testen
    M = MotorControl()
    M.forward(50)
    utime.sleep(0.5)
    M.backward(50)
    utime.sleep(0.5)
    M.left(30)
    utime.sleep(0.5)
    M.right(30)
    utime.sleep(0.5)
    M.stop()
