from FeatureService.AutoPicoGo import AutoPicoGo
from machine import Pin

###################Pin Config###################

###################Car Settings####################

autoPicoGo = AutoPicoGo()

autoPicoGo.calibrate()

while True:
    autoPicoGo.run()