import utime

class PicoTime():
    def __init__(self, library=utime):
        self.utime = library

    def ticks_ms(self):
        return self.utime.ticks_ms()
        
    def ticks_diff(self, end, start):
        return self.utime.ticks_diff(end, start)
    
    def has_time_elapsed(self, start_time, threshold_ms):
        current_time = self.ticks_ms()
        elapsed = self.ticks_diff(current_time, start_time)
        return elapsed >= threshold_ms
    
    def sleep_ms(self, ms):
        self.utime.sleep_ms(ms)