from Motor import MotorControl #importiert die Klasse MotorControl aus der Datei Motor.py
from machine import Pin
import time


M = MotorControl() #legt ein neues Objekt names M der Klasse MotorControl an
Buzzer = Pin(4, Pin.OUT) #Buzzer zum aktivieren des Pieptons

time.sleep(2) #wartet 2 Sekunden
M.forward(50) #fährt mit Geschwindigkeit 50% vorwärts
time.sleep(0.5) #wartet 0.5 Sekunden
M.left(100) #dreht mit Geschwindigkeit 100% nach links
Buzzer.value(1) #aktiviert den Piepton
time.sleep(2) #wartet 2 Sekunden
M.stop() #stoppt beide Motoren
Buzzer.value(0) #deaktiviert den Piepton










