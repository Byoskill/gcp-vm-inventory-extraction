import datetime


class Timeserie:
    timestamp = datetime.datetime.now()
    value: float = 0
    
    
    def __init__(self, timestamp, value ):    
        self.timestamp = timestamp
        self.value = value
    
    def value_in_gb(self) -> float: return self.value /1024 / 1024
        