from board import Board
from move import MOVELIST
import init

class EngineControls:
    def __init__(self):
        # we need all of these to control how long engine needs to think (search)
        self.starttime = 0
        self.stoptime = 0
        self.depth = 0
        self.depthset = 0
        self.timeset = 0
        self.movestogo = 0
        self.infinite = 0
        
        self.nodes = 0 # count of all the positions that the engine visited
        
        self.quit = 0 # quit if GUI wants to quit the search
        self.stopped = 0
        
        # fail high , fail high first
        self.fh = 0 # A "fail high" means that the evaluation of a move exceeded the beta value
        self.fhf = 0 # Fail High First refers to the situation where the first move evaluated in a position causes a fail high, This is a good sign because it means the engine is ordering its moves well. If the first move fails high, it indicates that the best move (or one of the best moves) was tried first, allowing the engine to prune the rest of the search tree early.

class Engine:
    MAX_ELO = 1500
    START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    def __init__(self, elo=1500):
        self.name = "UstaadJi"
        self.author = "Vanshu Galhotra"
        self.version = "1.0.0"
        self.elo = elo
        self.controls = EngineControls()
        self.board = Board()
        
        init.initialize()
        self.load_fen(fen=Engine.START_FEN)
        
    def legal_moves(self) -> list:
        mlist = MOVELIST()
        mlist.generate_all_moves(self.board)
        return mlist.get_move_list()
    
    def reset_board(self) -> None:
        pass
    
    def load_fen(self, fen: str) -> bool:
        return self.board.parse_fen(fen=fen)
        
    def get_fen(self) -> str:
        pass
    
    def make_move(self, move: str) -> bool:
        pass
    
    def is_move_legal(self, move: str) -> bool:
        pass
    
    def set_elo(self, elo: int) -> None:
        self.elo = elo
        
    def get_elo(self) -> int:
        return self.elo
    
    def evaluate(self) -> int:
        pass
    
    def best_move(self) -> str:
        pass