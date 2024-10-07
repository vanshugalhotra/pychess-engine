from debug import assert_condition
from constants import MAXGAMEMOVES

def isRepetition(board):
    for index in range(board.hisPly - board.fiftyMove, board.hisPly-1): # checking from only when last time fiftyMove was set to 0 because once fifty move is set to 0 there won't be no repetetions(captures and pawn moves cant repeat)
        if(board.posKey == board.history[index].posKey):
            assert_condition(index >=0 and index <= MAXGAMEMOVES)
            return True
        
    return False
