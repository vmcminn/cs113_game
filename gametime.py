class GameTime: 
    def __init__(self):
        self.qsec = 0
    
    def __call__(self):
        return self.qsec
        
    def inc(self):
        self.qsec += 1
        
    def as_seconds(self):
        return self.qsec/4
    
    def as_half_seconds(self):
        return self.qsec/2
        
    def as_quarter_seconds(self):
        return self.qsec
        
    def __str__(self):
        sec = self.qsec/4
        return '{:>2}:{:0>2}'.format(str(int(sec/60)), str(int(sec%60)))
