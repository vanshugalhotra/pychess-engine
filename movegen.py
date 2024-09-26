from globals import FilesBrd, RanksBrd
from constants import SQUARES, RANK, FILE, PIECE, COLORS, MFLAGPS
from debug import assert_condition
from board import CheckBoard
from validate import SqOnBoard
from data import PieceCol

TEST_FEN = "rnbqkb1r/pp1p1pPp/8/2p1pP2/1P1P4/3P3P/P1P1P3/RNBQKBNR w KQkq e6 0 1 "

def MOVE(fromSq, toSq, captured, prom, fl):
    return (fromSq | (toSq << 7) | (captured << 14) | (prom << 20) | fl)

def SQOFFBOARD(sq):
    return FilesBrd[sq] == SQUARES.OFFBOARD.value

def AddQuietMove(board, move, list):
    list.moves[list.count].move = move
    list.moves[list.count].score = 0
    list.count += 1
    
def AddCaptureMove(board, move, list):
    list.moves[list.count].move = move
    list.moves[list.count].score = 0
    list.count += 1
    
def AddEnPassantMove(board, move, list):
    list.moves[list.count].move = move
    list.moves[list.count].score = 0
    list.count += 1
    

def AddWhitePawnCapMove(board, fromSq, toSq, cap, list):
    if(RanksBrd[fromSq] == RANK.R7.value): # if a white pawn captures something from rank 7, then it is promotion move
        AddCaptureMove(board, MOVE(fromSq, toSq,cap,PIECE.wQ.value, 0), list) # promoted to white Queen
        AddCaptureMove(board, MOVE(fromSq, toSq,cap,PIECE.wR.value, 0), list) # promoted to white Rook
        AddCaptureMove(board, MOVE(fromSq, toSq,cap,PIECE.wB.value, 0), list) # promoted to white Bishop
        AddCaptureMove(board, MOVE(fromSq, toSq,cap,PIECE.wN.value, 0), list) # promoted to white Knight
    else: # if it is not an promotion move
        AddCaptureMove(board, MOVE(fromSq, toSq, cap, PIECE.EMPTY.value, 0), list)
        
def AddWhitePawnMove(board, fromSq, toSq, list): # same as above, the difference is it doesn't capture any piece
    if(RanksBrd[fromSq] == RANK.R7.value): # if a white pawn captures something from rank 7, then it is promotion move
        AddQuietMove(board, MOVE(fromSq, toSq,PIECE.EMPTY.value,PIECE.wQ.value, 0), list) # promoted to white Queen
        AddQuietMove(board, MOVE(fromSq, toSq,PIECE.EMPTY.value,PIECE.wR.value, 0), list) # promoted to white Rook
        AddQuietMove(board, MOVE(fromSq, toSq,PIECE.EMPTY.value,PIECE.wB.value, 0), list) # promoted to white Bishop
        AddQuietMove(board, MOVE(fromSq, toSq,PIECE.EMPTY.value,PIECE.wN.value, 0), list) # promoted to white Knight
    else: # if it is not an promotion move
        AddQuietMove(board, MOVE(fromSq, toSq, PIECE.EMPTY.value, PIECE.EMPTY.value, 0), list)

# generating moves for all pieces   
def GenerateAllMoves(board, list):
    
    assert_condition(CheckBoard(board))
    
    # generating white pawn moves
    list.count = 0
    pce = PIECE.EMPTY.value
    side = board.side
    sq = 0
    t_sq = 0
    
    if(side == COLORS.WHITE.value):
        # looping to total number of white pawns on the board
        for pceNum in range(0, board.pceNum[PIECE.wP.value]):
            sq = board.pList[PIECE.wP.value][pceNum] # to get the square on which there is a white Pawn
            assert_condition(SqOnBoard(sq))
            
            # if it is a no capture move
            if(board.pieces[sq + 10] == PIECE.EMPTY.value):
                AddWhitePawnMove(board, sq, sq+10, list) # board, fromSq, ToSq, list
                #
                if(RanksBrd[sq] == RANK.R2.value and board.pieces[sq + 20] == PIECE.EMPTY.value):
                    AddQuietMove(board, MOVE(sq, sq+20, PIECE.EMPTY.value, PIECE.EMPTY.value, MFLAGPS), list) # added a quite move, because there was no capture, also setted the Pawn Start Flag
              
            # if it is a capture move            
            if(not SQOFFBOARD(sq + 9) and PieceCol[board.pieces[sq + 9]] == COLORS.BLACK.value): # if the capturing piece is black
                AddWhitePawnCapMove(board, sq, sq+9, board.pieces[sq+9], list) # board, fromSq, ToSq, CapturedPiece, list
                
            if(not SQOFFBOARD(sq + 11) and PieceCol[board.pieces[sq + 11]] == COLORS.BLACK.value): # if the capturing piece is black
                AddWhitePawnCapMove(board, sq, sq+11, board.pieces[sq+11], list) # board, fromSq, ToSq, CapturedPiece, list
                      
    else: 
        pass

