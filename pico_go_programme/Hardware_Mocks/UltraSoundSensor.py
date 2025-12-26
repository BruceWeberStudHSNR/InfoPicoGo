
class UltraSoundSensor():

    def __init__(self, pin_in=14, pin_out=15):
        self._distance = 0

    def get_distance(self):
        return self._distance

    def set_distance(self, d):
        self._distance = d
