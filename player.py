class Player(object):

    def __init__(self, board, score):
        self.board = board
        self.score = score
        self.streams = []
        self.meadows = []

    def total(self):
        return sum([v for v in self.score.values()])
