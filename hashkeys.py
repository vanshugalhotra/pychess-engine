from constants import PIECE, BRD_SQ_NUM, SQUARES, COLORS
from debug import assert_condition
from helper import RAND_64

class PositionKey:
    PieceKeys = [[RAND_64() for _ in range(120)] for _ in range(13)]

    SideKey = RAND_64()
    CastleKeys = CastleKeys = [RAND_64() for _ in range(16)]

    def __init__(self):
        self.key = 0
        
    def hash_piece(self, piece, square) -> None:
        self.key ^= PositionKey.PieceKeys[piece][square]
        
    def hash_castle(self, castlePerm: int) -> None:
        self.key ^= PositionKey.CastleKeys[castlePerm]
        
    def hash_side(self) -> None:
        self.key ^= PositionKey.SideKey
        
    def hash_enPas(self, enPas: int) -> None:
        self.key ^= PositionKey.PieceKeys[PIECE.EMPTY.value][enPas]
        
    def generate_key(self, board) -> None:
        finalKey = 0
        piece = PIECE.EMPTY.value
        for sq in range(0, BRD_SQ_NUM):
            piece = board.pieces[sq]
            if(piece != SQUARES.OFFBOARD.value and piece != PIECE.EMPTY.value):
                assert_condition(piece >= PIECE.wP.value and piece <= PIECE.bK.value)
                finalKey ^= PositionKey.PieceKeys[piece][sq]
        
        if(board.side == COLORS.WHITE.value):
            finalKey ^= PositionKey.SideKey
            
        if(board.enPas != SQUARES.NO_SQ.value):
            assert_condition(board.enPas >= 0 and board.enPas < BRD_SQ_NUM)
            finalKey ^= PositionKey.PieceKeys[PIECE.EMPTY.value][board.enPas]
            
        assert_condition(board.castlePerm >= 0 and board.castlePerm <= 15)
        finalKey ^= PositionKey.CastleKeys[board.castlePerm]
        
        self.key = finalKey
