from constants import PIECE, COLORS, SQUARES
from data import PieceKnight, PieceKing, PieceRookQueen, PieceBishopQueen, PieceCol

# Knight Direction
KnDir = [-8, -19, -21, -12, 8, 19, 21, 12]

#Rook Direction
RkDir = [-1, -10, 1, 10]

#Bishop Direction
BiDir = [-9, -11, 11, 9]

#King Direction
KiDir = [-1, -10, 1, 10, -9, -11, 11, 9]

# isSquareAttacked(sq, side); is square "sq" attacked by "side"

def SqAttacked(sq, side, board):
    # checking for pawns
    if(side == COLORS.WHITE.value):
        if(board.pieces[sq - 11] == PIECE.wP.value or board.pieces[sq - 9] == PIECE.wP.value): # -9 -11 for white pieces, 
            return True
    else:
        if(board.pieces[sq + 11] == PIECE.bP.value or board.pieces[sq + 9] == PIECE.bP.value): # +9 and +11 for black pawns
            return True
        
    # checking for knights
    for i in range(0, 8): # looping on each square there can be a knight attacking
        pce = board.pieces[sq + KnDir[i]]
        if(PieceKnight[pce] and PieceCol[pce] == side):
            return True
        
    # rooks, queens
    for i in range(0, 4):
        dir = RkDir[i]
        t_sq = sq + dir
        pce = board.pieces[t_sq]
        while(pce != SQUARES.OFFBOARD.value): # for moving pieces, till they reach the board end
            if(pce != PIECE.EMPTY.value):
                if(PieceRookQueen[pce] and PieceCol[pce] == side):
                    return True
                break #if it hits another piece
            t_sq += dir
            pce = board.pieces[t_sq]
            
    # bishops, queens
    for i in range(0, 4):
        dir = BiDir[i]
        t_sq = sq + dir
        pce = board.pieces[t_sq]
        while(pce != SQUARES.OFFBOARD.value): # for moving pieces, till they reach the board end
            if(pce != PIECE.EMPTY.value):
                if(PieceBishopQueen[pce] and PieceCol[pce] == side):
                    return True
                break #if it hits another piece
            t_sq += dir
            pce = board.pieces[t_sq]
            
    # kings
    for i in range(0, 8):
        pce = board.pieces[sq + KiDir[i]]
        if(PieceKing[pce] and PieceCol[pce] == side):
            return True
            
    return False