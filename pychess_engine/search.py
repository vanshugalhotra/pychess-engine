from pychess_engine.debug import _assert_condition
from pychess_engine.constants import BRD_SQ_NUM, MAXDEPTH
from pychess_engine.misc import GetTimeMs
from pychess_engine.attack import is_square_attacked
from pychess_engine.board import Board
from pychess_engine.move import MOVE, MOVELIST

INFINITE = 30000
MATE = 29000

class Search:
    """
    The Search class implements the core search algorithm for a chess engine, including
    iterative deepening, alpha-beta pruning, and quiescence search. It optimizes move ordering
    using heuristics like killer moves and search history, while tracking the principal variation.

    Attributes:
        board (Board): The current board state being evaluated.
        info (EngineControls): Metadata for the search process, including nodes searched and time.

    Methods:
        update(board, info): Updates the current board and search info.
        _clear_for_search(): Resets search-related data and heuristics.
        _quiescene(alpha, beta): Performs quiescence search to evaluate tactical positions.
        _alpha_beta(alpha, beta, depth, do_null): Implements the alpha-beta pruning algorithm.
        iterative_deepening(): Performs iterative deepening search to find the best move.
    """
    def __init__(self, board: Board, info):
        self.board = board
        self.info = info

    def update(self, board, info) -> None:
        """Updates the current board and search info."""
        self.board=board
        self.info=info

    def _clear_for_search(self) -> None:
        """
        Resets all search-related data structures and counters to prepare for a new search.

        This method clears heuristics such as search history and killer moves, resets the
        principal variation table, and initializes counters like ply, nodes searched,
        and fail-high metrics to their default values.

        """
        for index in range(13):
            for index2 in range(BRD_SQ_NUM):
                self.board.searchHistory[index][index] = MOVE()

        for index in range(2):
            for index2 in range(MAXDEPTH):
                self.board.searchKillers[index][index2] = MOVE()

        self.board.PvTable._clear_table()
        self.board.ply = 0

        self.info.stopped = 0
        self.info.nodes = 0
        self.info.fh = 0
        self.info.fhf = 0

    # Horizon Effect: caused by depth limitation of the search algorithm. Lets say at the last depth White queen captures a knight and since its the last depth we stop evaluating further, so right now white is up a knight but what if black takes the white queen (But this move is not considered due to limited depth)
    def _quiescene(self, alpha: int, beta: int) -> int:
        """
        Performs quiescence search to mitigate the horizon effect by evaluating only non-quiet (capture) positions.

        The quiescence search extends beyond the regular search depth, evaluating only capture moves to
        ensure stable evaluation by avoiding premature conclusions on unstable positions. This method checks for
        repetitions, the fifty-move rule, and beta cutoffs to improve efficiency.

        Args:
            alpha (int): The lower bound of search value.
            beta (int): The upper bound of search value.

        Returns:
            int: The evaluated score of the quiescent position.
        """
        _assert_condition(self.board._check_board())
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
        mlist._generate_capture_moves(self.board)

        Legal = 0
        OldAlpha = alpha
        BestMove = 0
        Score = -INFINITE

        for MoveNum in range(mlist.count):
            mlist._pick_next_move(movenum=MoveNum)
            if(not self.board.make_move(mlist.moves[MoveNum])):
                continue
            Legal +=1
            Score = -self._quiescene(alpha=-beta, beta=-alpha)
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
            self.board.PvTable._store_pv_move(board=self.board, move=BestMove)

        return alpha

    # A beta cutoff occurs when the maximizing player finds a move that is so good that the minimizing player will avoid this line altogether.

    # An alpha cutoff occurs when the minimizing player finds a move that is so bad that the maximizing player will avoid this line altogether.

    def _alpha_beta(self, alpha: int, beta: int, depth: int, do_null) -> int:
        """
        Performs the Alpha-Beta pruning algorithm for a given search depth to improve search efficiency by pruning branches
        of the game tree that are not worth exploring.

        The Alpha-Beta algorithm enhances the minimax search by maintaining two values, alpha and beta, to prune unnecessary
        branches based on the evaluations of previous moves. The method evaluates positions recursively while applying
        beta and alpha cutoffs and adjusts search history and killer moves to guide the search.

        Args:
            alpha (int): The lower bound of the evaluation for the maximizing player.
            beta (int): The upper bound of the evaluation for the minimizing player.
            depth (int): The current search depth.
            do_null (bool): A flag indicating if null move pruning should be applied.

        Returns:
            int: The best score found for the given position, potentially pruned.
        """
        _assert_condition(self.board._check_board())

        if(depth == 0):
            return self._quiescene(alpha, beta)

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
        PvMove = self.board.PvTable._probe_pv_table(board=self.board)

        if(PvMove != 0):
            for MoveNum in range(mlist.count):
                if(mlist.moves[MoveNum].move == PvMove):
                    mlist.moves[MoveNum].score = 2000000 # will search this first
                    break

        for MoveNum in range(mlist.count):
            mlist._pick_next_move(movenum=MoveNum)
            if(not  self.board.make_move(mlist.moves[MoveNum])):
                continue
            Legal +=1
            Score = -self._alpha_beta(alpha=-beta, beta=-alpha, depth=depth-1, do_null=True)
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
            if(is_square_attacked(self.board.king_square[self.board.side], self.board.side ^ 1, self.board)):
                return -MATE + self.board.ply # how many moves it was to mate
            else: # stalemate
                return 0

        if(alpha != OldAlpha):
            self.board.PvTable._store_pv_move(board=self.board, move=BestMove)

        return alpha

    def iterative_deepening(self, display_calculation: bool) -> str:
        """
        Performs iterative deepening search, gradually increasing the search depth from 1 to a maximum depth. This method
        allows the engine to adjust to time constraints while ensuring progressively better evaluations.

        Iterative deepening combines the benefits of depth-first search and breadth-first search, providing the best of both.
        It allows the engine to maintain a principal variation (PV) for better pruning and move ordering, as well as
        heuristics like search history and killers.

        Returns:
            str: The best move found at the final depth.
        """
        # iterative deepening, search init
        # for depth = 1 to maxDepth, for each of these depths we then search with _alpha_beta
        # our depth depends on the time left on the clock, we don't want to search to depth 10 on first move and lose on time
        # iterative deepening means searching from depth 1 to depth n
        # ? why don't we just search directly on depth n
        # * because in iterative deepening first of all we will have our principal variation which will help in pruning more in _alpha_beta & Move Ordering. also we are maitaining the heurisitsc (searchHistory & searchKillers) which will help in move ordering

        bestMove = MOVE()
        bestScore = -INFINITE
        pvMoves = 0

        self._clear_for_search()

        #iterative deepening
        for currentDepth in range(1, self.info.depth+1):
            bestScore = self._alpha_beta(alpha=-INFINITE, beta=INFINITE, depth=currentDepth, do_null=True)

            # out of time?
            if(self.info.stopped):
                break

            pvMoves = self.board.PvTable._get_pv_line(board=self.board, depth=currentDepth)
            bestMove = self.board.PvArray[0]

            if(display_calculation):
                print(f"info score cp {bestScore} depth {currentDepth} nodes {self.info.nodes} time {GetTimeMs() - self.info.starttime}ms", end=" ")

                print("pv", end=" ")
                for pvNum in range(0, pvMoves):
                    print(f"{self.board.PvArray[pvNum].alpha_move()}", end=" ")
                print()
                if(self.info.fh):
                    print(f"Ordering: {(self.info.fhf / self.info.fh):.2f}")
                else:
                    print("Ordering: NAN")

        bestmove = bestMove.alpha_move()
        if(bestMove.move == 0):
            bestmove = "-"
        display_calculation and print(f"bestmove {bestmove}")
        return bestmove
