class ScoreColor:
    """A class to represent a score and color pair.
       This class will contain the score and color of a score in the following formats:
       
    """
    def __init__(self, score, color):        
        self.score = score
        self.color = color
    
    def __lt__(self, other):
        return self.score < other.score
    