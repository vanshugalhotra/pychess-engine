from globals import PieceKeys, SideKey, CastleKeys
from constants import PIECE, BRD_SQ_NUM, SQUARES, COLORS
from debug import assert_condition

def GeneratePosKey(board):
    finalKey = 0
    piece = PIECE.EMPTY.value
    for sq in range(0, BRD_SQ_NUM):
        piece = board.pieces[sq]
        if(piece != SQUARES.NO_SQ.value and piece != PIECE.EMPTY.value):
            assert_condition(piece >= PIECE.wP.value and piece <= PIECE.bK.value)
            finalKey ^= PieceKeys[piece][sq]
    
    if(board.side == COLORS.WHITE.value):
        finalKey ^= SideKey
        
        
    if(board.enPas != SQUARES.NO_SQ.value):
        assert_condition(board.enPas >= 0 and board.enPas < BRD_SQ_NUM)
        finalKey ^= PieceKeys[PIECE.EMPTY.value][board.enPas]
        
    assert_condition(board.castlePerm >= 0 and board.castlePerm <= 15)
    finalKey ^= CastleKeys[board.castlePerm]
    
    return finalKey
    