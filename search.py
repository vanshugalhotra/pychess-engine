from debug import assert_condition
from constants import MAXGAMEMOVES

def CheckUp(): # will be called after certain node
    # check if time up or interrupt from GUI
    pass

def isRepetition(board):
    for index in range(board.hisPly - board.fiftyMove, board.hisPly-1): # checking from only when last time fiftyMove was set to 0 because once fifty move is set to 0 there won't be no repetetions(captures and pawn moves cant repeat)
        if(board.posKey == board.history[index].posKey):
            assert_condition(index >=0 and index <= MAXGAMEMOVES)
            return True
        
    return False

def ClearForSearch(board, info): # clear all the stats , heuristics, searchHistory, searchKillers etc..
    pass

def AlphaBeta(alpha, beta, depth, board, info, DoNull):
    return 0

# Horizon Effect: caused by depth limitation of the search algorithm. Lets say at the last depth White queen captures a knight and since its the last depth we stop evaluating further, so right now white is up a knight but what if black takes the white queen (But this move is not considered due to limited depth)
# solution to the horizon effect is : quiescence search i.e evaluation only quiet positions (Without captures)
def Quiescence(alpha, beta, board, info):
    return 0

def SearchPosition(board, info): # class BOARD, class SEARCHINFO
    # iterative deepening, search init
    
    pass
    
