from debug import assert_condition
from constants import MAXGAMEMOVES, BRD_SQ_NUM, MAXDEPTH, MOVELIST, MFLAGCAP, FROMSQ, TOSQ
from pvtable import ClearPvTable, GetPvLine, StorePvMove, ProbePvTable
from misc import GetTimeMs
from input_output import PrMove
from validate import CheckBoard
from evaluate import EvalPosition
from movegen import GenerateAllMoves, GenerateAllCaps
from makemove import MakeMove, TakeMove
from attack import SqAttacked

INFINITE = 30000
MATE = 29000

def CheckUp(info): # will be called after certain node
    # check if time up or interrupt from GUI
    if(info.timeset == True and GetTimeMs() > info.stoptime):
        info.stopped = True

def isRepetition(board):
    for index in range(board.hisPly - board.fiftyMove, board.hisPly-1): # checking from only when last time fiftyMove was set to 0 because once fifty move is set to 0 there won't be no repetetions(captures and pawn moves cant repeat)
        if(board.posKey == board.history[index].posKey):
            assert_condition(index >=0 and index <= MAXGAMEMOVES)
            return True
        
    return False

def PickNextMove(movenum, mlist):
    """
    The function iterates through a list of moves and selects the move with the highest score (the most promising move) from the remaining moves. 
    It then swaps the selected move with the current move (movenum). This helps ensure the most promising move is evaluated first in AlphaBeta, which improves the chances of pruning.
    
    """
    bestScore = 0
    bestNum = movenum
    for index in range(movenum, mlist.count): # from given moveNum to end of movelist
        if(mlist.moves[index].score > bestScore):
            bestScore = mlist.moves[index].score
            bestNum = index
    # swapping it (move ordering)    
    mlist.moves[movenum], mlist.moves[bestNum] = mlist.moves[bestNum], mlist.moves[movenum]

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
    info.fh = 0
    info.fhf = 0


# Horizon Effect: caused by depth limitation of the search algorithm. Lets say at the last depth White queen captures a knight and since its the last depth we stop evaluating further, so right now white is up a knight but what if black takes the white queen (But this move is not considered due to limited depth)
# solution to the horizon effect is : quiescence search i.e evaluation only non-quiet positions (captures)
def Quiescence(alpha, beta, board, info): # only captures
    assert_condition(CheckBoard(board))
    if( (info.nodes & 2047) == 0): # means after every 2048th node
        CheckUp(info)
        
    info.nodes += 1
    
    if(isRepetition(board) or board.fiftyMove >= 100):
        return 0
    
    if(board.ply > MAXDEPTH - 1):
        return EvalPosition(board)
    
    Score = EvalPosition(board)
    
    if(Score >= beta):
        return beta
    
    if(Score > alpha):
        alpha = Score
    
    mlist = MOVELIST()
    GenerateAllCaps(board, mlist)
    
    Legal = 0
    OldAlpha = alpha
    BestMove = 0
    Score = -INFINITE
    
    for MoveNum in range(mlist.count):
        PickNextMove(MoveNum, mlist)
        if(not MakeMove(board, mlist.moves[MoveNum].move)):
            continue
        Legal +=1
        Score = -Quiescence(-beta, -alpha, board, info)
        TakeMove(board)
        if(info.stopped):
            return 0
        
        if(Score > alpha):
            if(Score >= beta): # beta cut off
                if(Legal == 1):
                    info.fhf += 1
                info.fh += 1
                return beta
            alpha = Score
            BestMove = mlist.moves[MoveNum].move

    if(alpha != OldAlpha):
        StorePvMove(board, BestMove)
    
    return alpha


# A beta cutoff occurs when the maximizing player finds a move that is so good that the minimizing player will avoid this line altogether.

# An alpha cutoff occurs when the minimizing player finds a move that is so bad that the maximizing player will avoid this line altogether.
def AlphaBeta(alpha, beta, depth, board, info, DoNull):
    
    assert_condition(CheckBoard(board))
    
    if(depth == 0):
        return Quiescence(alpha, beta, board, info)

    if( (info.nodes & 2047) == 0): # means after every 2048th node
        CheckUp(info)
    
    info.nodes += 1
    if(isRepetition(board) or board.fiftyMove >= 100):
        return 0
    
    if(board.ply > MAXDEPTH - 1):
        return EvalPosition(board)
    
    mlist = MOVELIST()
    GenerateAllMoves(board, mlist)
    
    Legal = 0
    OldAlpha = alpha
    BestMove = 0
    Score = -INFINITE
    PvMove = ProbePvTable(board)
    
    if(PvMove != 0):
        for MoveNum in range(mlist.count):
            if(mlist.moves[MoveNum].move == PvMove):
                mlist.moves[MoveNum].score = 2000000 # will search this first
                break
    
    for MoveNum in range(mlist.count):
        PickNextMove(MoveNum, mlist)
        if(not MakeMove(board, mlist.moves[MoveNum].move)):
            continue
        Legal +=1
        Score = -AlphaBeta(-beta, -alpha, depth-1, board, info, True)
        TakeMove(board)
        if(info.stopped):
            return 0
        
        if(Score > alpha):
            if(Score >= beta): # beta cut off
                """
                Fail High (FH) Update:

                Every time the engine prunes a branch because the evaluation of a move exceeds the beta value (a fail high), we increment the FH counter.
                This means the engine found a move that was good enough to stop searching the rest of the moves at that depth or node.
                
                Fail High First (FHF) Update:

                If the first move evaluated at a node causes a fail high, we increment both the FH counter and the FHF counter.
                This reflects that the move ordering was good, and the engine found the best move right away.
                """
                if(Legal == 1): # if first move caused beta cutoff
                    info.fhf += 1
                info.fh += 1
                # killer moves are those which causes beta cutoff and are not captures
                if(not (mlist.moves[MoveNum].move & MFLAGCAP)): # if not a capture move
                    board.searchKillers[1][board.ply] = board.searchKillers[0][board.ply]
                    board.searchKillers[0][board.ply] = mlist.moves[MoveNum].move
                return beta
            alpha = Score
            BestMove = mlist.moves[MoveNum].move
            if(not (mlist.moves[MoveNum].move & MFLAGCAP)): # not a capture
                board.searchHistory[board.pieces[FROMSQ(BestMove)]][TOSQ(BestMove)] += depth
    
    if(Legal == 0): # checkmate
        if(SqAttacked(board.KingSq[board.side], board.side^1, board)):
            return -MATE + board.ply # how many moves it was to mate
        else: # stalemate
            return 0
        
    if(alpha != OldAlpha):
        StorePvMove(board, BestMove)
    
    return alpha


def SearchPosition(board, info): # class BOARD, class SEARCHINFO
    # iterative deepening, search init
    # for depth = 1 to maxDepth, for each of these depths we then search with AlphaBeta
    # our depth depends on the time left on the clock, we don't want to search to depth 10 on first move and lose on time
    # iterative deepening means searching from depth 1 to depth n 
    # ? why don't we just search directly on depth n 
    # * because in iterative deepening first of all we will have our principal variation which will help in pruning more in AlphaBeta & Move Ordering. also we are maitaining the heurisitsc (searchHistory & searchKillers) which will help in move ordering
    
    
    bestMove = 0
    bestScore = -INFINITE
    pvMoves = 0
    
    ClearForSearch(board, info)
    
    #iterative deepening
    for currentDepth in range(1, info.depth+1):
        bestScore = AlphaBeta(-INFINITE, INFINITE, currentDepth, board, info, True) # alpha beta
        
        # out of time?
        if(info.stopped):
            break
    
        pvMoves = GetPvLine(currentDepth, board)
        bestMove = board.PvArray[0]
        
        print(f"Depth: {currentDepth} Score: {bestScore} Move: {PrMove(bestMove)} Nodes: {info.nodes}")
        
        print("PV: ", end=" ")
        for pvNum in range(0, pvMoves):
            print(f"{PrMove(board.PvArray[pvNum])}", end="  ")
        print()
        if(info.fh):
            print(f"Ordering: {(info.fhf / info.fh):.2f}")
        else:
            print("Ordering: NAN")