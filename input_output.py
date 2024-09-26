from globals import FilesBrd, RanksBrd
from constants import FROMSQ, TOSQ, PROMOTED, CAPTURED
from data import PieceKnight, PieceBishopQueen, PieceRookQueen

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