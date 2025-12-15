import utime
from Motor import MotorControl
from machine import Pin

#Demo für eine Hindernisumgehung mit den beiden Infrarotsensoren vorne
#Wenn keiner der Sensoren etwas sieht, fährt der er PicoGo vorwärts
#Wenn linke Sensor etwas sieht, dreht sich der PicoGo nach rechts
#Wenn der rechte oder beide Sensoren etwas sehen, dreht sich der Roboter nach links

M = MotorControl()
DSR = Pin(2, Pin.IN) 
DSL = Pin(3, Pin.IN)

while True:
    DR_status = DSR.value()
    DL_status = DSL.value()
    
    #DL_status == 0 beschreibt, dass der linke Sensor etwas sieht
    #DR_status == 0 beschreibt, dass der rechte Sensor etwas sieht

    if((DL_status == 0) and (DR_status == 0)):
        M.left(10)
    elif((DL_status == 0) and (DR_status == 1)):
        M.right(10)
    elif((DL_status == 1) and (DR_status == 0)):
        M.left(10)
    else:
        M.forward(20)
        
    utime.sleep_ms(10)
