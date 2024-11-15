from hashkeys import PositionKey

class UNDO:
    def __init__(self):
        self.move = 0 # the move number
        self.castlePerm = 0
        self.enPas = -1
        self.fiftyMove = 0
        self.posKey = PositionKey() #unqiue position key (object of PositionKey Class)
        # castling information