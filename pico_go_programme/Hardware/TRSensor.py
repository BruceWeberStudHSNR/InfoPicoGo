from machine import Pin
import machine
import time
import rp2


#Bietet Methoden zu Nutzung der IR-Sensoren unten am PicoGo um Linien zu folgen
#Für Sie sind vor allem die Methoden calibrate und realLine wichtig
#Wie Sie diese Methoden anwenden, wird in den Demos Line-Tracking.py bzw. Line-Tracking2.py dargestellt

@rp2.asm_pio(out_shiftdir=0, autopull=True, pull_thresh=12, autopush=True, push_thresh=12, sideset_init=(rp2.PIO.OUT_LOW), out_init=rp2.PIO.OUT_LOW)
def spi_cpha0():
    out(pins, 1)             .side(0x0)   [1]
    in_(pins, 1)             .side(0x1)   [1]
        
class TRSensor():
    def __init__(self):
        self.numSensors = 5
        self.calibratedMin = [0] * self.numSensors
        self.calibratedMax = [1023] * self.numSensors
        self.last_value = 0
        self.Clock     = 6
        self.Address   = 7
        self.DataOut   = 27
        self.CS        = Pin(28, Pin.OUT)
        self.CS.value(1)
        self.sm = rp2.StateMachine(1, spi_cpha0, freq=4*200000, sideset_base=Pin(self.Clock, Pin.OUT), out_base=Pin(self.Address, Pin.OUT), in_base=Pin(self.DataOut, Pin.IN))
        self.sm.active(1)
        
    
    #Gibt die (unkalibrierten) Messungen der Sensoren zurück
    def AnalogRead(self):
        value = [0]*(self.numSensors+1)
        
        #Read Channel~channe5 AD value
        for j in range(0,self.numSensors+1):
            self.CS.value(0)
            #set channe
            self.sm.put(j << 28)
            #get last channe value
            value[j] = self.sm.get() & 0xfff
            self.CS.value(1)
            value[j] >>= 2
        time.sleep_ms(2)
        return value[1:]
    

    #Liest die Sensoren 10 mal zur Kalibrierung aus
    #Ein Beispiel wie man damit Kalibriert, finden Sie in Line-Tracking.py bzw. Line-Tracking2.py
    def calibrate(self):
        max_sensor_values = [0]*self.numSensors
        min_sensor_values = [0]*self.numSensors
        for j in range(0,10):
        
            sensor_values = self.AnalogRead();
            
            for i in range(0,self.numSensors):
            
                # set the max we found THIS time
                if((j == 0) or max_sensor_values[i] < sensor_values[i]):
                    max_sensor_values[i] = sensor_values[i]

                # set the min we found THIS time
                if((j == 0) or min_sensor_values[i] > sensor_values[i]):
                    min_sensor_values[i] = sensor_values[i]

        # record the min and max calibration values
        for i in range(0,self.numSensors):
            if(min_sensor_values[i] > self.calibratedMin[i]):
                self.calibratedMin[i] = min_sensor_values[i]
            if(max_sensor_values[i] < self.calibratedMax[i]):
                self.calibratedMax[i] = max_sensor_values[i]
        

    #Gibt für jeden Sensor einen Wert zwischen 0 und 1000 zurück
    #0 ist der minimale Wert der bei der Kalibrierung festgestellt wurde und 1000 der maximal
    def readCalibrated(self):
        value = 0
        sensor_values = self.AnalogRead()
        
        for i in range (0,self.numSensors):
            denominator = self.calibratedMax[i] - self.calibratedMin[i]

            if(denominator != 0):
                value = (sensor_values[i] - self.calibratedMin[i])* 1000 / denominator

            if(value < 0):
                value = 0
            elif(value > 1000):
                value = 1000

            sensor_values[i] = int(value)

        return sensor_values


    #Genau wie die Methode readCalibrated, gibt aber zusätzlich eine geschätze Position des Roboters im Verhältnis zu Linie zurück
    #0 bedeutet, dass die Linie direkt unter Sensor 1 ist
    #1000 bedeutet, dass die Linie direkt unter Sensor 2 ist
    #----
    #4000 bedeutet, dass die Linie direkt unter Sensor 5 ist
    #white_line kann auf 1 gesetzt werden um weiße Linien auf dunklem Hintergrund zu tracken
    def readLine(self, white_line = 0):
        sensor_values = self.readCalibrated()
        avg = 0
        sum = 0
        on_line = 0
        for i in range(0,self.numSensors):
            value = sensor_values[i]
            if(white_line):
                value = 1000-value
            # keep track of whether we see the line at all
            if(value > 200):
                on_line = 1
                
            # only average in values that are above a noise threshold
            if(value > 50):
                avg += value * (i * 1000);  # this is for the weighted total,
                sum += value;               # this is for the denominator 

        if(on_line != 1):
            # If it last read to the left of center, return 0.
            if(self.last_value < (self.numSensors - 1)*1000/2):
                #print("left")
                self.last_value = 0;

            # If it last read to the right of center, return the max.
            else:
                #print("right")
                self.last_value = (self.numSensors - 1)*1000
        else:
            self.last_value = avg/sum

        return int(self.last_value),sensor_values

if __name__ == '__main__':

    print("\nTRSensor Test Program ...\r\n")
    TRS=TRSensor()
    while True:
        print(TRS.AnalogRead())
        time.sleep(0.1)
                