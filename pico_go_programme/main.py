import utime
from AutoFeatures.AutoPicoGo import AutoPicoGo
from AutoFeatures.Operation import PicoTime
from Hardware import MotorControl, TRSensor, UltraSoundSensor, LEDControl, Buzzer
from Hardware_Mocks import MockTRSensor,MockUltraSoundSensor
from AutoFeatures.ObstacleAversion import ObstacleDetection
from AutoFeatures.LineFollowing import LineFollowService,LineDetection
from AutoFeatures.ObstacleAversion import AvoidObstacleService
from AutoFeatures.Operation import PicoPilot, LightOperator



autoPicoGo = None

def autoFactory(mock=False):
    forward_speed=20
    turn_speed=15
    led_mode="LINE_AND_OBSTACLE"
    
    is_checking_for_obstacles=True
    obstacle_recognition_distance = 70
    obstacle_recognition_time = 300
    obstacle_remember_time = 1000
    turntime = 1000
    dashtime = 2000
    recogniselinetime=100
    forgetlinetime=500
    onlinethreshhold=300

    # Hardware
    Motor=MotorControl.MotorControl()
    Led=LEDControl.LEDControl()
    Buzzer_=Buzzer.Buzzer()
    Tr_sensor = TRSensor.TRSensor()
    TimeService = PicoTime.PicoTime(utime)
    Ultra_sound = UltraSoundSensor.UltraSoundSensor()
    if (mock):
        Tr_sensor = MockTRSensor.MockTRSensor()
        Ultra_sound = MockUltraSoundSensor.MockUltraSoundSensor()

    # Service
    Pilot = PicoPilot.PicoPilot(
            Motor=Motor,
            TimeService=TimeService,
            default_speed=forward_speed
        )
    Light_Operator = LightOperator.LightOperator(
            Led=Led)

    Line_Detection = LineDetection.LineDetection(
            TRSensor=Tr_sensor,
            TimeService=TimeService,
            on_line_threshold=onlinethreshhold,
            forget_line_time=forgetlinetime,
            recognize_line_time=recogniselinetime
        )
    LineFollow_Service = LineFollowService.LineFollowService(
            Pilot=Pilot,
            LineDetection=Line_Detection,
            dash_time=dashtime, 
            turn_time=turntime)
    Obstacle_Detection = ObstacleDetection.ObstacleDetection(
            Ultra_sound, 
            TimeService,
            obstacle_recognition_distance=obstacle_recognition_distance,
            obstacle_recognition_time=obstacle_recognition_time,
            obstacle_remember_time=obstacle_remember_time)        
    AvoidObstacle_Service = AvoidObstacleService.AvoidObstacleService(
            TimeService, 
            Motor, 
            Led, 
            Obstacle_Detection )


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
        Buzzer=Buzzer_,
        Pilot=Pilot,
        LightOperator=Light_Operator,
        LineDetection=Line_Detection,
        LineFollowing=LineFollow_Service,
        ObstacleAversion=AvoidObstacle_Service,
        ObstacleDetection=Obstacle_Detection,
        speed_levels=[])
    assert autoPicoGo is not None, "AutoPicoGo instance required"
    
    return autoPicoGo

autoPicoGo = autoFactory(mock=False)


autoPicoGo.calibrate_line_sensors()

while True:
    autoPicoGo.run()
