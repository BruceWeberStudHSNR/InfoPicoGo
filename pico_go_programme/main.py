from AutoFeatures.AutoPicoGo import AutoPicoGo
from Hardware import MotorControl, TRSensor, UltraSoundSensor, LEDControl, Buzzer
from Hardware_Mocks import MockTRSensor,MockUltraSoundSensor

autoPicoGo = None

def autoFactory(mock=False):
    forward_speed=20, 
    turn_speed=25, 
    is_checking_for_obstacles=True,
    Motor=MotorControl.MotorControl(),
    Led=LEDControl.LEDControl(),
    Buzzer_=Buzzer.Buzzer()
    Ultra_sound=None,
    Tr_sensor=None
    if (mock):
        Tr_sensor = MockTRSensor.MockTRSensor()
        Ultra_sound = MockUltraSoundSensor.MockUltraSoundSensor()
    else:
        Tr_sensor = MockTRSensor.MockTRSensor()
        Ultra_sound = MockUltraSoundSensor.MockUltraSoundSensor()

    autoPicoGo = AutoPicoGo(
        forward_speed=forward_speed, 
        turn_speed=turn_speed, 
        is_checking_for_obstacles=is_checking_for_obstacles,
        Motor=Motor,
        Tr_sensor=Tr_sensor,
        Led=Led,
        Ultra_sound=Ultra_sound,
        Buzzer=Buzzer_)
    return autoPicoGo

autoPicoGo = autoFactory()

assert autoPicoGo is not None, "IRSensor instance required"

autoPicoGo.calibrate_line_sensors()

while True:
    autoPicoGo.run()
