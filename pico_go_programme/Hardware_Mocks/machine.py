
class Pin():
    def __init__(self):
        self.In = 0
        self.Out = 0
        self.__mockValue = 0
        
    def value(self):
        return self.__mockValue
    
    def setValue(self, value):
        self.__mockValue = value