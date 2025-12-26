
class MockTRSensor():
    def __init__(self):
        self.__mockAnalogRead = 0
        self.__mockPosition = 0
        self.__mockSensorValues = [0,0,0,0,0]
        
    def setAnalogRead(self, value):
        self.__mockAnalogRead = value

    def AnalogRead(self):
        return self.__mockAnalogRead
    
    def calibrate(self):
        pass
        
    def readCalibrated(self):
        return self.__mockSensorValues
    
    def setCalibrated(self, value):
        self.__mockSensorValues = value

    def setPosition(self,value):
        self.__mockPosition = value

    def readLine(self, white_line = 0):
        return self.__mockPosition,self.readCalibrated()