from AutoPicoGo import AutoPicoGo
from machine import Pin

###################Pin Config###################



autoPicoGo = AutoPicoGo()

while True:
    autoPicoGo.automated_drive()
    autoPicoGo.update_buzzer()