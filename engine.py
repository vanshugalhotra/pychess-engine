from board import Board
from move import MOVELIST, MOVE
import init
from fens import START_FEN
from misc import GetTimeMs, ReadInput
from helper import execution_time
from search import Search
from constants import MAXDEPTH

class EngineControls:
    def __init__(self):
        # we need all of these to control how long engine needs to think (search)
        self.starttime = 0
        self.stoptime = 0
        self.depth = 0
        self.depthset = 0
        self.timeset = False
        self.movestogo = 0
        self.infinite = 0
        
        self.nodes = 0 # count of all the positions that the engine visited
        
        self.quit = 0 # quit if GUI wants to quit the search
        self.stopped = 0
        
        # fail high , fail high first
        self.fh = 0 # A "fail high" means that the evaluation of a move exceeded the beta value
        self.fhf = 0 # Fail High First refers to the situation where the first move evaluated in a position causes a fail high, This is a good sign because it means the engine is ordering its moves well. If the first move fails high, it indicates that the best move (or one of the best moves) was tried first, allowing the engine to prune the rest of the search tree early.
        
    def __str__(self):
        return self.display()
        
    def display(self):
        search_time = f"{round(self.stoptime - self.starttime, 2)}ms"
        if(not self.stoptime):
            search_time = "Not Defined"
        return (f"Engine Controls: Search Time: {search_time} \tDepth:{self.depth} \tTime Set: {'Yes' if self.timeset else 'No'} \tMovesToGo: {self.movestogo} \tInfinite Mode: {'On' if self.infinite else 'Off'}\n")
        
    def check_up(self):
        # check if time up or interrupt from GUI
        if (self.timeset == True and GetTimeMs() > self.stoptime):
            self.stopped = True
            
        ReadInput(self)

class Engine:
    MAX_ELO = 1500
    def __init__(self, elo=1500):
        self.name = "UstaadJi"
        self.author = "Vanshu Galhotra"
        self.version = "1.0.0"
        self.elo = elo
        self.controls = EngineControls()
        self.board = Board()
        self.search = Search(self.board, self.controls)
        
        init.initialize()
        self.load_fen(fen=START_FEN)
        
    def legal_moves(self) -> list:
        mlist = MOVELIST()
        mlist.generate_all_moves(board=self.board)
        return mlist.get_move_list()
    
    def reset_board(self) -> None:
        self.board.reset_board()
        self.board.parse_fen(fen=START_FEN)
    
    def load_fen(self, fen: str) -> bool:
        return self.board.parse_fen(fen=fen)
        
    def get_fen(self) -> str:
        pass
    
    def make_move(self, move: str) -> bool:
        enc_move = MOVE.parse_move(alpha_move=move, board=self.board)
        if(enc_move == MOVE.NOMOVE):
            return False
        return self.board.make_move(move=enc_move) # if move is not legal it returns True
    
    def is_move_legal(self, move: str) -> bool:
        enc_move = MOVE.parse_move(alpha_move=move, board=self.board)
        return enc_move == MOVE.NOMOVE
    
    def set_elo(self, elo: int) -> None:
        self.elo = elo
        
    def get_elo(self) -> int:
        return self.elo
    
    def evaluate(self) -> int:
        return self.board.evaluate_position()
    
    @execution_time
    def best_move(self, depth=MAXDEPTH, movestogo=30, movetime=None, increment=0, time=None) -> str:
        self.controls.depth = depth # depth set according to elo
        self.controls.movestogo = movestogo
        self.controls.starttime = GetTimeMs()
        
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


        self.search.update(board=self.board, info=self.controls)
        print(self.controls)
        
        return self.search.iterative_deepening()