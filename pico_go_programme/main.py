from AutoFeatures.AutoPicoGo import AutoPicoGo
import utime
from Hardware import MotorControl, TRSensor, UltraSoundSensor, LEDControl, Buzzer
from Hardware_Mocks import MockTRSensor,MockUltraSoundSensor

autoPicoGo = None

def autoFactory(mock=False):
    forward_speed=40
    turn_speed=25
    led_mode="LINE"
    is_checking_for_obstacles=True
    Motor=MotorControl.MotorControl()
    Led=LEDControl.LEDControl()
    Buzzer_=Buzzer.Buzzer()
    Ultra_sound=None
    Tr_sensor=None
    TimeService = utime
    if (mock):
        Tr_sensor = MockTRSensor.MockTRSensor()
        Ultra_sound = MockUltraSoundSensor.MockUltraSoundSensor()
    else:
        Tr_sensor = TRSensor.TRSensor()
        Ultra_sound = UltraSoundSensor.UltraSoundSensor()

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
    return autoPicoGo

autoPicoGo = autoFactory(mock=False)

assert autoPicoGo is not None, "AutoPicoGo instance required"

autoPicoGo.calibrate_line_sensors()

while True:
    autoPicoGo.run()
