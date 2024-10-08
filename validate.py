from constants import COLORS, PIECE, RANK, SQUARES
from bitboards import CountBits, PopBit
from globals import Sq64ToSq120, RanksBrd, FilesBrd
from data import PieceBig, PieceMaj, PieceMin, PieceCol, PieceVal
from hashkeys import GeneratePosKey
from debug import assert_condition, DEBUG

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


def CheckBoard(board):
    if(not DEBUG):
        return True
    
    t_pceNum = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    t_bigPce = [0,0]
    t_majPce = [0,0]
    t_minPce = [0,0]
    t_material = [0,0]
    
    t_pawns = [0, 0, 0]
    t_pawns[COLORS.WHITE.value] = board.pawns[COLORS.WHITE.value]
    t_pawns[COLORS.BLACK.value] = board.pawns[COLORS.BLACK.value]
    t_pawns[COLORS.BOTH.value] = board.pawns[COLORS.BOTH.value]
    
    
    # check piece lists
    for t_piece in range(PIECE.wP.value, PIECE.bK.value+1):
        for t_pce_num in range(0, board.pceNum[t_piece]): # lets say we have 3 white pawns, this loop will loop form 0 - 2
            sq120 = board.pList[t_piece][t_pce_num] # getting the sqaure of the pawn
            assert_condition(board.pieces[sq120] == t_piece, message="Mismatch between the pList and pieces (12x10 board)") # checking if on actual 12x10 board, that piece exists on that square or not
            
    # check piece count and other counters
    for sq64 in range(0, 64):
        sq120 = Sq64ToSq120[sq64]
        t_piece = board.pieces[sq120]
        if(t_piece != 0):
            t_pceNum[t_piece] += 1 #incrementing the no. of pieces, 
            colour = PieceCol[t_piece]
            
            if(PieceBig[t_piece]):
                t_bigPce[colour] += 1
            if(PieceMin[t_piece]):
                t_minPce[colour] += 1
            if(PieceMaj[t_piece]):
                t_majPce[colour] += 1
            
            t_material[colour] += PieceVal[t_piece]
        
    for t_piece in range(PIECE.wP.value, PIECE.bK.value+1):
        assert_condition(t_pceNum[t_piece] == board.pceNum[t_piece], message="Piece Number Not Matched!") #checking if the piece number on the board is equal to the piece num we calculated
        
    # check pawn bitboards
    pcount = CountBits(t_pawns[COLORS.WHITE.value])
    assert_condition(pcount == board.pceNum[PIECE.wP.value], message="Mismatch between WHITE Pawns Bitboard and No. of White Pawns")
    pcount = CountBits(t_pawns[COLORS.BLACK.value])
    assert_condition(pcount == board.pceNum[PIECE.bP.value], message="Mismatch between BLACK Pawns Bitboard and No. of BLack Pawns")
    pcount = CountBits(t_pawns[COLORS.BOTH.value])
    assert_condition(pcount == board.pceNum[PIECE.wP.value] + board.pceNum[PIECE.bP.value], message="Mismatch between BOTH Pawns Bitboard and No. of BOTH Pawns")
    
    #check bitboards square
    tp = t_pawns[COLORS.WHITE.value]
    while(tp):
        sq64, tp = PopBit(tp)
        assert_condition(board.pieces[Sq64ToSq120[sq64]] == PIECE.wP.value, message="WHITE Pawn on bitboard and actual Board not Matched!!")
        
    tp = t_pawns[COLORS.BLACK.value]
    while(tp):
        sq64, tp = PopBit(tp)
        assert_condition(board.pieces[Sq64ToSq120[sq64]] == PIECE.bP.value, message="BLACK Pawn on bitboard and actual Board not Matched!!")
        
    tp = t_pawns[COLORS.BOTH.value]
    while(tp):
        sq64, tp = PopBit(tp)
        assert_condition((board.pieces[Sq64ToSq120[sq64]] == PIECE.wP.value) or (board.pieces[Sq64ToSq120[sq64]] == PIECE.bP.value), message="WHITE or BLACK Pawn on bitboard and actual Board not Matched!!")
        
    assert_condition(t_material[COLORS.WHITE.value] == board.material[COLORS.WHITE.value] and t_material[COLORS.BLACK.value] == board.material[COLORS.BLACK.value], message="Material Value Not Matched!!")
    
    assert_condition(t_minPce[COLORS.WHITE.value] == board.minPce[COLORS.WHITE.value] and t_minPce[COLORS.BLACK.value] == board.minPce[COLORS.BLACK.value], message="Number of Min Pieces not Matched!!")
    
    assert_condition(t_majPce[COLORS.WHITE.value] == board.majPce[COLORS.WHITE.value] and t_majPce[COLORS.BLACK.value] == board.majPce[COLORS.BLACK.value], message="Number of Maj Pieces not Matched!!")
    
    assert_condition(t_bigPce[COLORS.WHITE.value] == board.bigPce[COLORS.WHITE.value] and t_bigPce[COLORS.BLACK.value] == board.bigPce[COLORS.BLACK.value], message="Number of Big (Non-Pawn) Pieces not Matched!!")
    
    assert_condition(board.side == COLORS.WHITE.value or board.side == COLORS.BLACK.value, message="SIDE can either be WHITE or BLACK")

    assert_condition(GeneratePosKey(board) == board.posKey, message="PosKey not Matched!!")
    
    assert_condition(board.enPas == SQUARES.NO_SQ.value or (RanksBrd[board.enPas] == RANK.R6.value and board.side == COLORS.WHITE.value) or (RanksBrd[board.enPas] == RANK.R3.value and board.side == COLORS.BLACK.value), message="Invalid EnPas Square") # enPas square is either on rank 3 or rank 6
    
    assert_condition(board.pieces[board.KingSq[COLORS.WHITE.value]] == PIECE.wK.value, message="WHITE King Square not Matched!!")
    assert_condition(board.pieces[board.KingSq[COLORS.BLACK.value]] == PIECE.bK.value, message="BLACK King Square not Matched!!")
    
    return True
    