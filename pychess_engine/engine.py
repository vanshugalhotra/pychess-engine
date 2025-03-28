from pychess_engine.board import Board
from pychess_engine.move import MOVELIST, MOVE
from pychess_engine.init import initialize
from pychess_engine.fens import START_FEN
from pychess_engine.misc import GetTimeMs, ReadInput
from pychess_engine.helper import execution_time
from pychess_engine.search import Search
from pychess_engine.perft import PerftTest

class EngineControls:
    """
    Manages the settings and metrics for the engine's search process.

    Attributes:
        starttime (int): Start time of the search in milliseconds.
        stoptime (int): Stop time of the search in milliseconds.
        depth (int): Maximum depth for search.
        depthset (int): Flag for setting depth-based search.
        timeset (bool): Whether a specific time limit is set.
        movestogo (int): Number of moves to complete within the time limit.
        infinite (int): Flag to indicate infinite search mode.
        nodes (int): Total positions visited during search.
        quit (int): Flag for quitting search on GUI request.
        stopped (int): Indicates if search has been manually stopped.
        fh (int): Count of fail-high occurrences during alpha-beta pruning.
        fhf (int): Count of fail-high occurrences on the first move.
    """
    elo_to_depth = {
        300  : 1,
        700  : 2,
        1000 : 3,
        1300 : 4,
        1500 : 5,
        1700 : 6
    }
    def __init__(self):
        self.starttime = 0
        self.stoptime = 0
        self.depth = 0
        self.depthset = 0
        self.timeset = False
        self.movestogo = 0
        self.infinite = 0
        self.nodes = 0
        self.quit = 0
        self.stopped = 0

        # fail high , fail high first
        self.fh = 0 # A "fail high" means that the evaluation of a move exceeded the beta value
        self.fhf = 0 # Fail High First refers to the situation where the first move evaluated in a position causes a fail high, This is a good sign because it means the engine is ordering its moves well. If the first move fails high, it indicates that the best move (or one of the best moves) was tried first, allowing the engine to prune the rest of the search tree early.

    def __str__(self):
        """
        Returns a formatted string with the current engine control settings.

        Returns:
            str: Formatted representation of engine controls for display.
        """
        return self.display()

    def display(self):
        """
        Displays the engine control settings in a formatted string.

        Returns:
            str: Information about search time, depth, and other control settings.
        """
        search_time = f"{round(self.stoptime - self.starttime, 2)}ms"
        if(not self.stoptime):
            search_time = "Not Defined"
        return (f"Engine Controls: Search Time: {search_time} \tDepth:{self.depth} \tTime Set: {'Yes' if self.timeset else 'No'} \tMovesToGo: {self.movestogo} \tInfinite Mode: {'On' if self.infinite else 'Off'}\n")

    def check_up(self):
        """
        Checks if the allotted search time has expired or if an interrupt request was made.

        Sets the `stopped` attribute to True if the current time exceeds the stop time.
        """
        if (self.timeset == True and GetTimeMs() > self.stoptime):
            self.stopped = True

        ReadInput(self)

class Engine:
    """
    Provides core functionality for move generation, board management,
    evaluation, configuration of search controls and Searching the best move.

    Attributes:
        name (str): Name of the chess engine.
        author (str): Author of the engine.
        version (str): Version of the engine.
        elo (int): ELO rating that adjusts the depth of search.
        controls (EngineControls): Manages search control settings.
        board (Board): Represents the current board state.
        search (Search): Manages search algorithms and move evaluation.

    Methods:
        - legal_moves() -> list: Generates a list of all legal moves from the current board state.
        - reset_board() -> None: Resets the board to the initial position.
        - load_fen(fen: str) -> bool: Loads a board position from a FEN string.
        - get_fen() -> str: Returns the current board position as a FEN string.
        - make_move(move: str) -> bool: Makes a move on the board if it’s legal.
        - is_move_legal(move: str) -> bool: Checks if a move is legal.
        - set_elo(elo: int) -> None: Sets the ELO rating, adjusting the search depth.
        - get_elo() -> int: Returns the current ELO rating.
        - evaluate() -> int: Evaluates the current board position.
        - best_move(depth=MAXDEPTH, movestogo=30, movetime=None, increment=0, time=None) -> str:
        Determines the best move based on search parameters and constraints.

    """
    MAX_ELO = 1700
    def __init__(self, elo=1500):
        self.name = "UstaadJi"
        self.author = "Vanshu Galhotra"
        self.version = "1.0.0"
        self.elo = elo
        self.controls = EngineControls()
        self.board = Board()
        self.search = Search(self.board, self.controls)

        initialize()
        self.load_fen(fen=START_FEN)

    def legal_moves(self) -> list:
        """
        Generates all legal moves from the current board position.

        Returns:
            list: List of all possible moves (algebraic notation like e2e4) from the current position.
        """
        mlist = MOVELIST()
        mlist.generate_all_moves(board=self.board)
        return mlist._get_move_list()

    def reset_board(self) -> None:
        """Resets the board to the initial starting position."""
        self.board.reset_board()
        self.board.parse_fen(fen=START_FEN)

    def load_fen(self, fen: str) -> bool:
        """
        Loads a position from a FEN string.

        Args:
            fen (str): FEN string representing the board state.

        Returns:
            bool: True if the FEN string is parsed successfully, False otherwise.
        """
        return self.board.parse_fen(fen=fen)

    def get_fen(self) -> str:
        """
        Retrieves the current position as a FEN string.

        Returns:
            str: FEN string representing the current board state.
        """
        return self.board.get_fen()

    def make_move(self, move: str) -> bool:
        """
        Attempts to make a move on the board.

        Args:
            move (str): Move in algebraic notation (e.g., "e2e4").

        Returns:
            bool: True if the move is successfully made, False if the move is illegal.
        """
        enc_move = MOVE.parse_move(alpha_move=move, board=self.board)
        if(enc_move == MOVE.NOMOVE):
            return False
        return self.board.make_move(move=enc_move) # if move is not legal it returns True

    def is_move_legal(self, move: str) -> bool:
        """
        Checks if a move is legal on the current board.

        Args:
            move (str): Move in algebraic notation (e.g., "e2e4").

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        enc_move = MOVE.parse_move(alpha_move=move, board=self.board)
        return not enc_move == MOVE.NOMOVE

    def set_elo(self, elo: int) -> None:
        """
        Sets the ELO rating for the engine, influencing search depth.

        Args:
            elo (int): New ELO rating for the engine.
        """
        self.elo = elo

    def get_elo(self) -> int:
        """
        Retrieves the current ELO rating of the engine.

        Returns:
            int: The current ELO rating.
        """
        return self.elo

    def evaluate(self) -> int:
        """
        Evaluates the current board position.

        Returns:
            int: Evaluation score of the position.
        """
        return self.board.evaluate_position()

    @execution_time
    def best_move(self, depth=None, movestogo=30, movetime=None, increment=0, time=None, display_calculation=True) -> str:
        """
        Determines the best move using the specified search depth or time constraints.

        Args:
            depth (int, optional): Search depth for the engine.
            movestogo (int, optional): Number of moves to manage within the available time.
            movetime (int, optional): Time allocated for this move only.
            increment (int, optional): Additional time (increment) per move.
            time (int, optional): Total time available for the current search phase.
            display_calculation (bool, Optional): Whether wants to display the calculation part

        Returns:
            str: Best move in algebraic notation.
        """
        try:
            self.controls.movestogo = movestogo
            self.controls.starttime = GetTimeMs()

            if depth is None:
                depth = next((d for elo, d in sorted(EngineControls.elo_to_depth.items()) if self.elo <= elo), 6)

            self.controls.depth = depth

            if movetime:
                self.controls.movestogo = 1  # Only consider this move
                self.controls.timeset = True
                self.controls.stoptime = self.controls.starttime + movetime
            elif time:
                # Split available time across remaining moves
                self.controls.timeset = True
                time_per_move = time / movestogo
                buffer_time = 50  # To be safe
                self.controls.stoptime = self.controls.starttime + time_per_move + increment - buffer_time

            # Update search settings and initiate iterative deepening
            self.search.update(board=self.board, info=self.controls)
            if(display_calculation):
                print(self.controls)

            result = self.search.iterative_deepening(display_calculation=display_calculation)
        except Exception:
            print("Something went Wrong!")
        return result

    def print_board(self) -> None:
        self.board.print_board()

    def perft_test(self, depth=3) -> None:
        """Perft Testing"""
        PerftTest(depth=depth, board=self.board)