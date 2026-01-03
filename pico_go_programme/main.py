from AutoFeatures.AutoPicoGo import AutoPicoGo
from AutoFeatures.Operation import PicoTime
import utime
from Hardware import MotorControl, TRSensor, UltraSoundSensor, LEDControl, Buzzer
from Hardware_Mocks import MockTRSensor,MockUltraSoundSensor

autoPicoGo = None

def autoFactory(mock=False):
    forward_speed=40
    turn_speed=25
    led_mode="AVOIDING_OBSTACLE"
    is_checking_for_obstacles=True
    Motor=MotorControl.MotorControl()
    Led=LEDControl.LEDControl()
    Buzzer_=Buzzer.Buzzer()
    Tr_sensor = TRSensor.TRSensor()
    TimeService = PicoTime.PicoTime(utime)
    Ultra_sound = UltraSoundSensor.UltraSoundSensor()
    if (mock):
        Tr_sensor = MockTRSensor.MockTRSensor()
        Ultra_sound = MockUltraSoundSensor.MockUltraSoundSensor()

    autoPicoGo = AutoPicoGo(
        forward_speed=forward_speed, 
        turn_speed=turn_speed, 
        led_mode=led_mode,
        is_checking_for_obstacles=is_checking_for_obstacles,
        Motor=Motor,
        TimeService=TimeService,
        Tr_sensor=Tr_sensor,
        Led=Led,
        Ultra_sound=Ultra_sound,
        Buzzer=Buzzer_)
    assert autoPicoGo is not None, "AutoPicoGo instance required"
    
    return autoPicoGo

autoPicoGo = autoFactory(mock=False)


autoPicoGo.calibrate_line_sensors()

while True:
    autoPicoGo.run()
