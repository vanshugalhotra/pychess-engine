from pychessengine.constants import Pieces, Colors, Squares
from pychessengine.globals import FilesBrd

def SqOnBoard(sq):
    return 0 if FilesBrd[sq] == Squares.OFFBOARD else 1

def SideValid(side):
    return 1 if (side == Colors.WHITE or side == Colors.BLACK) else 0

def FileRankValid(fr):
    return 1 if (fr >= 0 and fr <= 7) else 0

def PieceValidEmpty(pce):
    return 1 if (pce >= Pieces.EMPTY and pce <= Pieces.bK) else 0

def PieceValid(pce):
    return 1 if (pce >= Pieces.wP and pce <= Pieces.bK) else 0
