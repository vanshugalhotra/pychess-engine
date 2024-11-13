from debug import assert_condition
from constants import BRD_SQ_NUM, MAXDEPTH
from misc import GetTimeMs
from attack import is_sqaure_attacked
from board import Board
from move import MOVE, MOVELIST

INFINITE = 30000
MATE = 29000

class Search:
    def __init__(self, board: Board, info):
        self.board = board
        self.info = info
        
    def update(self, board, info):
        self.board=board
        self.info=info
        
    def clear_for_search(self): # clear all the stats, heuristics, searchHistory, seachKillers etc...
        for index in range(13):
            for index2 in range(BRD_SQ_NUM):
                self.board.searchHistory[index][index] = MOVE()
                
        for index in range(2):
            for index2 in range(MAXDEPTH):
                self.board.searchKillers[index][index2] = MOVE()
                
        self.board.PvTable.clear_table()
        self.board.ply = 0
        
        self.info.stopped = 0
        self.info.nodes = 0
        self.info.fh = 0
        self.info.fhf = 0
        
    # Horizon Effect: caused by depth limitation of the search algorithm. Lets say at the last depth White queen captures a knight and since its the last depth we stop evaluating further, so right now white is up a knight but what if black takes the white queen (But this move is not considered due to limited depth)
    # solution to the horizon effect is : quiescence search i.e evaluation only non-quiet positions (captures)
    def quiescene(self, alpha: int, beta: int) -> int:
        assert_condition(self.board.check_board())
        if( (self.info.nodes & 2047) == 0): # means after every 2048th node
            self.info.check_up()
            
        self.info.nodes += 1
        
        if(self.board.is_repetition() or self.board.fiftyMove >= 100):
            return 0
        
        if(self.board.ply > MAXDEPTH - 1):
            return self.board.evaluate_position()
        
        Score = self.board.evaluate_position()
        
        if(Score >= beta):
            return beta
        
        if(Score > alpha):
            alpha = Score
        
        mlist = MOVELIST()
        mlist.generate_capture_moves(self.board)
        
        Legal = 0
        OldAlpha = alpha
        BestMove = 0
        Score = -INFINITE
        
        for MoveNum in range(mlist.count):
            mlist.pick_next_move(movenum=MoveNum)
            if(not self.board.make_move(mlist.moves[MoveNum])):
                continue
            Legal +=1
            Score = -self.quiescene(alpha=-beta, beta=-alpha)
            self.board.take_move()
            if(self.info.stopped):
                return 0
            
            if(Score > alpha):
                if(Score >= beta): # beta cut off
                    if(Legal == 1):
                        self.info.fhf += 1
                    self.info.fh += 1
                    return beta
                alpha = Score
                BestMove = mlist.moves[MoveNum]

        if(alpha != OldAlpha):
            self.board.PvTable.store_pv_move(board=self.board, move=BestMove)
        
        return alpha
    
    # A beta cutoff occurs when the maximizing player finds a move that is so good that the minimizing player will avoid this line altogether.

    # An alpha cutoff occurs when the minimizing player finds a move that is so bad that the maximizing player will avoid this line altogether.

    def AlphaBeta(self, alpha: int, beta: int, depth: int, doNull):
        assert_condition(self.board.check_board)
        
        if(depth == 0):
            return self.quiescene(alpha, beta)

        if( (self.info.nodes & 2047) == 0): # means after every 2048th node
            self.info.check_up()
        
        self.info.nodes += 1
        if(self.board.is_repetition() or self.board.fiftyMove >= 100):
            return 0
        
        if(self.board.ply > MAXDEPTH - 1):
            return self.board.evaluate_position()
        
        mlist = MOVELIST()
        mlist.generate_all_moves(self.board)
        
        Legal = 0
        OldAlpha = alpha
        BestMove = 0
        Score = -INFINITE
        PvMove = self.board.PvTable.probe_pv_table(board=self.board)
        
        if(PvMove != 0):
            for MoveNum in range(mlist.count):
                if(mlist.moves[MoveNum].move == PvMove):
                    mlist.moves[MoveNum].score = 2000000 # will search this first
                    break
        
        for MoveNum in range(mlist.count):
            mlist.pick_next_move(movenum=MoveNum)
            if(not  self.board.make_move(mlist.moves[MoveNum])):
                continue
            Legal +=1
            Score = -self.AlphaBeta(alpha=-beta, beta=-alpha, depth=depth-1, doNull=True)
            self.board.take_move()
            if(self.info.stopped):
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
                        self.info.fhf += 1
                    self.info.fh += 1
                    # killer moves are those which causes beta cutoff and are not captures
                    if(not (mlist.moves[MoveNum].move & MOVE.FLAG_CAP)): # if not a capture move
                        self.board.searchKillers[1][self.board.ply] = self.board.searchKillers[0][self.board.ply]
                        self.board.searchKillers[0][self.board.ply] = mlist.moves[MoveNum]
                    return beta
                alpha = Score
                BestMove = mlist.moves[MoveNum]
                if(not (mlist.moves[MoveNum].move & MOVE.FLAG_CAP)): # not a capture
                    self.board.searchHistory[self.board.pieces[BestMove.FROMSQ()]][BestMove.TOSQ()].score += depth
        
        if(Legal == 0): # checkmate
            if(is_sqaure_attacked(self.board.KingSq[self.board.side], self.board.side^1, self.board)):
                return -MATE + self.board.ply # how many moves it was to mate
            else: # stalemate
                return 0
            
        if(alpha != OldAlpha):
            self.board.PvTable.store_pv_move(board=self.board, move=BestMove)
        
        return alpha
    
    
    def iterative_deepening(self) -> str:
        # iterative deepening, search init
        # for depth = 1 to maxDepth, for each of these depths we then search with AlphaBeta
        # our depth depends on the time left on the clock, we don't want to search to depth 10 on first move and lose on time
        # iterative deepening means searching from depth 1 to depth n 
        # ? why don't we just search directly on depth n 
        # * because in iterative deepening first of all we will have our principal variation which will help in pruning more in AlphaBeta & Move Ordering. also we are maitaining the heurisitsc (searchHistory & searchKillers) which will help in move ordering
        
        bestMove = MOVE()
        bestScore = -INFINITE
        pvMoves = 0
        
        self.clear_for_search()
        
        #iterative deepening
        for currentDepth in range(1, self.info.depth+1):
            bestScore = self.AlphaBeta(alpha=-INFINITE, beta=INFINITE, depth=currentDepth, doNull=True)
            
            # out of time?
            if(self.info.stopped):
                break
        
            pvMoves = self.board.PvTable.get_pv_line(board=self.board, depth=currentDepth)
            bestMove = self.board.PvArray[0]
            
            print(f"info score cp {bestScore} depth {currentDepth} nodes {self.info.nodes} time {GetTimeMs() - self.info.starttime}ms", end=" ")
            
            print("pv", end=" ")
            for pvNum in range(0, pvMoves):
                print(f"{self.board.PvArray[pvNum].alpha_move()}", end=" ")
            print()
            if(self.info.fh):
                print(f"Ordering: {(self.info.fhf / self.info.fh):.2f}")
            else:
                print("Ordering: NAN")
                
        print(f"bestmove {bestMove.alpha_move()}")
        return bestMove.alpha_move()
    