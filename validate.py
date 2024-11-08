from constants import COLORS, PIECE, SQUARES
from globals import FilesBrd

def SqOnBoard(sq):
    return 0 if FilesBrd[sq] == SQUARES.OFFBOARD.value else 1

def SideValid(side):
    return 1 if (side == COLORS.WHITE.value or side == COLORS.BLACK.value) else 0

def FileRankValid(fr):
    return 1 if (fr >= 0 and fr <= 7) else 0

def PieceValidEmpty(pce):
    return 1 if (pce >= PIECE.EMPTY.value and pce <= PIECE.bK.value) else 0

def PieceValid(pce):
    return 1 if (pce >= PIECE.wP.value and pce <= PIECE.bK.value) else 0
