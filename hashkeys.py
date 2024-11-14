from constants import BRD_SQ_NUM, Pieces, Colors, Squares
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
        self.key ^= PositionKey.PieceKeys[Pieces.EMPTY][enPas]
        
    def generate_key(self, board) -> None:
        finalKey = 0
        piece = Pieces.EMPTY
        for sq in range(0, BRD_SQ_NUM):
            piece = board.pieces[sq]
            if(piece != Squares.OFFBOARD and piece != Pieces.EMPTY):
                assert_condition(piece >= Pieces.wP and piece <= Pieces.bK)
                finalKey ^= PositionKey.PieceKeys[piece][sq]
        
        if(board.side == Colors.WHITE):
            finalKey ^= PositionKey.SideKey
            
        if(board.enPas != Squares.NO_SQ):
            assert_condition(board.enPas >= 0 and board.enPas < BRD_SQ_NUM)
            finalKey ^= PositionKey.PieceKeys[Pieces.EMPTY][board.enPas]
            
        assert_condition(board.castlePerm >= 0 and board.castlePerm <= 15)
        finalKey ^= PositionKey.CastleKeys[board.castlePerm]
        
        self.key = finalKey
