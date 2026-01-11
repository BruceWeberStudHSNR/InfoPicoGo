import utime

class PicoTime():
    def __init__(self, library=utime):
        self.utime = library

    def current_time(self):
        return self.utime.ticks_ms()

    def ticks_ms(self):
        return self.utime.ticks_ms()
        
    def ticks_diff(self, end, start):
        return self.utime.ticks_diff(end, start)
    
    def has_time_elapsed(self, start_time, threshold_ms):
        elapsed = self.elapsed_time(start_time)
        return elapsed >= threshold_ms
    
    def sleep_ms(self, ms):
        self.utime.sleep_ms(ms)

    def elapsed_time(self,start):
        current_time = self.ticks_ms()
        elapsed = self.ticks_diff(current_time, start)
        return elapsed