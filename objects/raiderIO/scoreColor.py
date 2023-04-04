class ScoreColor:
    def __init__(self, score, color):        
        self.score = score
        self.color = color
    
    def __lt__(self, other):
        return self.score < other.score
    
