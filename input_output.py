from globals import FilesBrd, RanksBrd
from constants import FROMSQ, TOSQ, PROMOTED, FR2SQ, MOVELIST, PIECE
from data import PieceKnight, PieceBishopQueen, PieceRookQueen
from debug import assert_condition
from validate import SqOnBoard, CheckBoard
from movegen import GenerateAllMoves

NOMOVE = 0

# for printing the square in algebraic form
def PrSq(sq):
    file = FilesBrd[sq]
    rank = RanksBrd[sq]
    SqStr = "{}{}".format(chr(ord('a') + file), chr(ord('1') + rank))
    
    return SqStr

# for printing the move in algebraic form
def PrMove(move):
    ff = FilesBrd[FROMSQ(move)] # file from 
    rf = RanksBrd[FROMSQ(move)] # rank from 
    ft = FilesBrd[TOSQ(move)] # file TO
    rt = RanksBrd[TOSQ(move)] # rank TO
    
    promoted = PROMOTED(move) # promoted piece value
    
    if(promoted):
        pchar = 'q'
        if(PieceKnight[promoted]): # if promoted piece was a knight
            pchar = 'n'
        elif(PieceRookQueen[promoted] and not PieceBishopQueen[promoted]):
            pchar = 'r'
        elif(not PieceRookQueen[promoted] and PieceBishopQueen[promoted]):
            pchar = 'b'
        MvStr = "{}{}{}{}{}".format(chr(ord('a') + ff), chr(ord('1') + rf), chr(ord('a') + ft), chr(ord('1') + rt), pchar)
    else:
        MvStr = "{}{}{}{}".format(chr(ord('a') + ff), chr(ord('1') + rf), chr(ord('a') + ft), chr(ord('1') + rt))
        
    return MvStr

# parsing a move from user input, like a2a3 --> getting the specific move from this string
def parseMove(userMove, board):
    assert_condition(CheckBoard(board))
    
    if(userMove[1] > '8' or userMove[1] < '1'):
        return NOMOVE
    if(userMove[3] > '8' or userMove[3] < '1'):
        return NOMOVE
    if(userMove[0] > 'h' or userMove[0] < 'a'):
        return NOMOVE
    if(userMove[2] > 'h' or userMove[2] < 'a'):
        return NOMOVE
    
    fromSq = FR2SQ(ord(userMove[0]) - ord('a'), ord(userMove[1]) - ord('1'))
    toSq = FR2SQ(ord(userMove[2]) - ord('a'), ord(userMove[3]) - ord('1'))
    
    assert_condition(SqOnBoard(fromSq) and SqOnBoard(toSq))
    list = MOVELIST()
    GenerateAllMoves(board, list)
    Move = NOMOVE
    PromPce = PIECE.EMPTY.value
    
    for MoveNum in range(0, list.count): # traversing the move list
        Move = list.moves[MoveNum].move # getting the move
        if(FROMSQ(Move) == fromSq and TOSQ(Move) == toSq): # if both the to and from sqaures are same, then move is also same, provided promoted piece can be different
            PromPce = PROMOTED(Move)
            if(PromPce != PIECE.EMPTY.value): # if there is a promotion, we need to check
                if(PieceRookQueen[PromPce] and not PieceBishopQueen[PromPce] and userMove[4] == 'r'): # promoted piece is a rook
                    return Move
                elif(not PieceRookQueen[PromPce] and PieceBishopQueen[PromPce] and userMove[4] == 'b'): # promoted piece is bishop
                    return Move
                elif(PieceBishopQueen[PromPce] and PieceRookQueen[PromPce] and userMove[4] == 'q'): #is a queen
                    return Move
                elif(PieceKnight[PromPce] and userMove[4] == 'n'): 
                    return Move
                continue
            return Move # else , if there was no promotion, then indeed move has matched, 
    
    return NOMOVE # if we didn't found the move in movelist
    
    

def PrintMoveList(list):
    print("MoveList: ")
    for i in range(0, list.count):
        move = list.moves[i].move
        score = list.moves[i].score
        
        print(f"Move: {i+1} --> {PrMove(move)} (Score: {score})")
    print(f"MoveList Total {list.count} Moves: \n")
    