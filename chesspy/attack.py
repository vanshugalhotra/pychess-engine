from pychessengine.constants import Pieces, Colors, Squares
from pychessengine.globals import PieceKnight, PieceKing, PieceRookQueen, PieceBishopQueen, PieceCol
from pychessengine.validate import SqOnBoard, SideValid, PieceValidEmpty
from pychessengine.debug import _assert_condition

# Knight Direction
knight_direction = [-8, -19, -21, -12, 8, 19, 21, 12]

#Rook Direction
rook_direction = [-1, -10, 1, 10]

#Bishop Direction
bishop_direction = [-9, -11, 11, 9]

#King Direction
king_direction = [-1, -10, 1, 10, -9, -11, 11, 9]


def is_sqaure_attacked(square: int, side: int, board) -> bool:
    
    """
    Determines if a given square is attacked by any piece of a specified (opposite) side.

    Args:
        square (int): The square index to check for attacks.
        side (int): The color of the attacking side (e.g., `Colors.WHITE` or `Colors.BLACK`).
        board (Board): The current board state.

    Returns:
        bool: True if the square is attacked, otherwise False.

    """
    
    _assert_condition(SqOnBoard(square))
    _assert_condition(SideValid(side))
    _assert_condition(board._check_board())
    
    # checking for pawns
    if(side == Colors.WHITE):
        if(board.pieces[square - 11] == Pieces.wP or board.pieces[square - 9] == Pieces.wP): # -9 -11 for white pieces, 
            return True
    else:
        if(board.pieces[square + 11] == Pieces.bP or board.pieces[square + 9] == Pieces.bP): # +9 and +11 for black pawns
            return True
        
    # checking for knights
    for i in range(0, 8): # looping on each square there can be a knight attacking
        pce = board.pieces[square + knight_direction[i]]
        if(PieceValidEmpty(pce) and PieceKnight[pce] and PieceCol[pce] == side):
            return True
        
    # rooks, queens
    for i in range(0, 4):
        dir = rook_direction[i]
        t_sq = square + dir
        pce = board.pieces[t_sq]
        while(pce != Squares.OFFBOARD): # for moving pieces, till they reach the board end
            if(pce != Pieces.EMPTY):
                if(PieceRookQueen[pce] and PieceCol[pce] == side):
                    return True
                break #if it hits another piece
            t_sq += dir
            pce = board.pieces[t_sq]
            
    # bishops, queens
    for i in range(0, 4):
        dir = bishop_direction[i]
        t_sq = square + dir
        pce = board.pieces[t_sq]
        while(pce != Squares.OFFBOARD): # for moving pieces, till they reach the board end
            if(pce != Pieces.EMPTY):
                if(PieceBishopQueen[pce] and PieceCol[pce] == side):
                    return True
                break #if it hits another piece
            t_sq += dir
            pce = board.pieces[t_sq]
            
    # kings
    for i in range(0, 8):
        pce = board.pieces[square + king_direction[i]]
        if(PieceValidEmpty(pce) and PieceKing[pce] and PieceCol[pce] == side):
            return True
            
    return False