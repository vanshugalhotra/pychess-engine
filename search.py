from debug import assert_condition
from constants import BRD_SQ_NUM, MAXDEPTH
from misc import GetTimeMs, ReadInput
from attack import is_sqaure_attacked
from board import Board
from move import MOVE, MOVELIST
from helper import execution_time

INFINITE = 30000
MATE = 29000

def CheckUp(info): # will be called after certain node
    # check if time up or interrupt from GUI
    if(info.timeset == True and GetTimeMs() > info.stoptime):
        info.stopped = True
        
    ReadInput(info)

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

def ClearForSearch(board: Board, info): # clear all the stats , heuristics, searchHistory, searchKillers etc..
    for index in range(13):
        for index2 in range(BRD_SQ_NUM):
            board.searchHistory[index][index] = MOVE()
            
    for index in range(2):
        for index2 in range(MAXDEPTH):
            board.searchKillers[index][index2] = MOVE()
            
    board.PvTable.clear_table()
    board.ply = 0
    
    info.stopped = 0
    info.nodes = 0
    info.fh = 0
    info.fhf = 0

# Horizon Effect: caused by depth limitation of the search algorithm. Lets say at the last depth White queen captures a knight and since its the last depth we stop evaluating further, so right now white is up a knight but what if black takes the white queen (But this move is not considered due to limited depth)
# solution to the horizon effect is : quiescence search i.e evaluation only non-quiet positions (captures)
def Quiescence(alpha, beta, board: Board, info): # only captures
    assert_condition(board.check_board())
    if( (info.nodes & 2047) == 0): # means after every 2048th node
        CheckUp(info)
        
    info.nodes += 1
    
    if(board.is_repetition() or board.fiftyMove >= 100):
        return 0
    
    if(board.ply > MAXDEPTH - 1):
        return board.evaluate_position()
    
    Score = board.evaluate_position()
    
    if(Score >= beta):
        return beta
    
    if(Score > alpha):
        alpha = Score
    
    mlist = MOVELIST()
    mlist.generate_capture_moves(board)
    
    Legal = 0
    OldAlpha = alpha
    BestMove = 0
    Score = -INFINITE
    
    for MoveNum in range(mlist.count):
        PickNextMove(MoveNum, mlist)
        if(not board.make_move(mlist.moves[MoveNum])):
            continue
        Legal +=1
        Score = -Quiescence(-beta, -alpha, board, info)
        board.take_move()
        if(info.stopped):
            return 0
        
        if(Score > alpha):
            if(Score >= beta): # beta cut off
                if(Legal == 1):
                    info.fhf += 1
                info.fh += 1
                return beta
            alpha = Score
            BestMove = mlist.moves[MoveNum]

    if(alpha != OldAlpha):
        board.PvTable.store_pv_move(board=board, move=BestMove)
    
    return alpha

# A beta cutoff occurs when the maximizing player finds a move that is so good that the minimizing player will avoid this line altogether.

# An alpha cutoff occurs when the minimizing player finds a move that is so bad that the maximizing player will avoid this line altogether.
def AlphaBeta(alpha, beta, depth: int, board:Board, info, DoNull):
    
    assert_condition(board.check_board)
    
    if(depth == 0):
        return Quiescence(alpha, beta, board, info)

    if( (info.nodes & 2047) == 0): # means after every 2048th node
        CheckUp(info)
    
    info.nodes += 1
    if(board.is_repetition() or board.fiftyMove >= 100):
        return 0
    
    if(board.ply > MAXDEPTH - 1):
        return board.evaluate_position()
    
    mlist = MOVELIST()
    mlist.generate_all_moves(board)
    
    Legal = 0
    OldAlpha = alpha
    BestMove = 0
    Score = -INFINITE
    PvMove = board.PvTable.probe_pv_table(board=board)
    
    if(PvMove != 0):
        for MoveNum in range(mlist.count):
            if(mlist.moves[MoveNum].move == PvMove):
                mlist.moves[MoveNum].score = 2000000 # will search this first
                break
    
    for MoveNum in range(mlist.count):
        PickNextMove(MoveNum, mlist)
        if(not  board.make_move(mlist.moves[MoveNum])):
            continue
        Legal +=1
        Score = -AlphaBeta(-beta, -alpha, depth-1, board, info, True)
        board.take_move()
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
                if(not (mlist.moves[MoveNum].move & MOVE.FLAG_CAP)): # if not a capture move
                    board.searchKillers[1][board.ply] = board.searchKillers[0][board.ply]
                    board.searchKillers[0][board.ply] = mlist.moves[MoveNum]
                return beta
            alpha = Score
            BestMove = mlist.moves[MoveNum]
            if(not (mlist.moves[MoveNum].move & MOVE.FLAG_CAP)): # not a capture
                board.searchHistory[board.pieces[BestMove.FROMSQ()]][BestMove.TOSQ()].score += depth
    
    if(Legal == 0): # checkmate
        if(is_sqaure_attacked(board.KingSq[board.side], board.side^1, board)):
            return -MATE + board.ply # how many moves it was to mate
        else: # stalemate
            return 0
        
    if(alpha != OldAlpha):
        board.PvTable.store_pv_move(board=board, move=BestMove)
    
    return alpha

@execution_time
def SearchPosition(board: Board, info): # class BOARD, class SEARCHINFO
    # iterative deepening, search init
    # for depth = 1 to maxDepth, for each of these depths we then search with AlphaBeta
    # our depth depends on the time left on the clock, we don't want to search to depth 10 on first move and lose on time
    # iterative deepening means searching from depth 1 to depth n 
    # ? why don't we just search directly on depth n 
    # * because in iterative deepening first of all we will have our principal variation which will help in pruning more in AlphaBeta & Move Ordering. also we are maitaining the heurisitsc (searchHistory & searchKillers) which will help in move ordering
    
    bestMove = MOVE()
    bestScore = -INFINITE
    pvMoves = 0
    
    ClearForSearch(board, info)
    
    #iterative deepening
    for currentDepth in range(1, info.depth+1):
        bestScore = AlphaBeta(-INFINITE, INFINITE, currentDepth, board, info, True) # alpha beta
        
        # out of time?
        if(info.stopped):
            break
    
        pvMoves = board.PvTable.get_pv_line(board=board, depth=currentDepth)
        bestMove = board.PvArray[0]
        
        print(f"info score cp {bestScore} depth {currentDepth} nodes {info.nodes} time {GetTimeMs() - info.starttime}ms", end=" ")
        
        print("pv", end=" ")
        for pvNum in range(0, pvMoves):
            print(f"{board.PvArray[pvNum].alpha_move()}", end=" ")
        print()
        if(info.fh):
            print(f"Ordering: {(info.fhf / info.fh):.2f}")
        else:
            print("Ordering: NAN")
            
    print(f"bestmove {bestMove.alpha_move()}")
    