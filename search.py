from debug import assert_condition
from constants import MAXGAMEMOVES, BRD_SQ_NUM, MAXDEPTH
from pvtable import ClearPvTable, GetPvLine
from misc import GetTimeMs
from math import inf
from input_output import PrMove

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
    for index in range(13):
        for index2 in range(BRD_SQ_NUM):
            board.searchHistory[index][index] = 0
            
    for index in range(2):
        for index2 in range(MAXDEPTH):
            board.searchKillers[index][index2] = 0
            
    ClearPvTable(board.PvTable)
    board.ply = 0
    
    info.starttime = GetTimeMs()
    info.stopped = 0
    info.nodes = 0

def AlphaBeta(alpha, beta, depth, board, info, DoNull):
    return 0

# Horizon Effect: caused by depth limitation of the search algorithm. Lets say at the last depth White queen captures a knight and since its the last depth we stop evaluating further, so right now white is up a knight but what if black takes the white queen (But this move is not considered due to limited depth)
# solution to the horizon effect is : quiescence search i.e evaluation only quiet positions (Without captures)
def Quiescence(alpha, beta, board, info):
    return 0

def SearchPosition(board, info): # class BOARD, class SEARCHINFO
    # iterative deepening, search init
    # for depth = 1 to maxDepth, for each of these depths we then search with AlphaBeta
    # our depth depends on the time left on the clock, we don't want to search to depth 10 on first move and lose on time
    # iterative deepening means searching from depth 1 to depth n 
    # ? why don't we just search directly on depth n 
    # * because in iterative deepening first of all we will have our principal variation which will help in pruning more in AlphaBeta & Move Ordering. also we are maitaining the heurisitsc (searchHistory & searchKillers) which will help in move ordering
    
    
    bestMove = 0
    bestScore = -inf
    pvMoves = 0
    
    ClearForSearch(board, info)
    
    #iterative deepening
    for currentDepth in range(1, info.depth+1):
        bestScore = AlphaBeta(-inf, inf, currentDepth, board, info, True) # alpha beta
        
        # out of time?
    
        pvMoves = GetPvLine(currentDepth, board)
        bestMove = board.PvArray[0]
        
        print(f"Depth: {currentDepth} Score: {bestScore} Move: {PrMove(bestMove)} Nodes: {info.nodes}")
        
        for pvNum in range(0, pvMoves):
            print(f"{PrMove(board.PvArray[pvNum])}", end="  ")
        print()