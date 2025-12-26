from AutoFeatures.AutoPicoGo import AutoPicoGo
from machine import Pin
import utime

###################Pin Config###################

###################Car Settings####################

autoPicoGo = AutoPicoGo(
    forward_speed=100, 
    turn_speed=20, 
    is_checking_for_obstacles=True)

autoPicoGo.calibrate()

while True:
    autoPicoGo.run()