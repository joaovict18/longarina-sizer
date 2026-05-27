class SparSegment:
    
    def __init__(self, y_start, y_end, section):
        self.y_start = y_start
        self.y_end = y_end
        self.section = section

    def contains(self, y):
        return self.y_start <= y <= self.y_end