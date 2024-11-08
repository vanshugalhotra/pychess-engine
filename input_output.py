from constants import FR2SQ, PIECE
from data import PieceKnight, PieceBishopQueen, PieceRookQueen
from debug import assert_condition
from validate import SqOnBoard, CheckBoard
from move import MOVELIST

NOMOVE = 0

# parsing a move from user input, like a2a3 --> getting the specific move from this string
def parseMove(userMove: str, board):
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
    list.generate_all_moves(board)
    Move = NOMOVE
    PromPce = PIECE.EMPTY.value
    
    for MoveNum in range(0, list.count): # traversing the move list
        Move = list.moves[MoveNum].move # getting the move of MOVE()
        if(Move.FROMSQ() == fromSq and Move.TOSQ() == toSq): # if both the to and from sqaures are same, then move is also same, provided promoted piece can be different
            PromPce = Move.PROMOTED()
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
        
        print(f"Move: {i+1} --> {move.alpha_move()} (Score: {score})")
    print(f"MoveList Total {list.count} Moves: \n")
    