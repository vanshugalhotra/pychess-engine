from enum import Enum
from random import getrandbits

BRD_SQ_NUM = 120
MAXGAMEMOVES = 2048
MAXPOSITIONMOVES = 256
MAXDEPTH = 64

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FEN1 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
FEN2 = "rnbqkbnr/pp1pppp p/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
FEN3 = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
FEN4 = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"

class PIECE(Enum):
    EMPTY = 0
    wP = 1 # white pawn
    wN = 2 # white Knight
    wB = 3 # white bishop
    wR = 4
    wQ = 5
    wK = 6
    bP = 7
    bN = 8
    bB = 9
    bR = 10
    bQ = 11
    bK = 12
    
class FILE(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7
    NONE = 8
    
class RANK(Enum):
    R1 = 0
    R2 = 1
    R3 = 2
    R4 = 3
    R5 = 4
    R6 = 5
    R7 = 6
    R8 = 7
    RNONE = 8
    
class COLORS(Enum):
    WHITE = 0
    BLACK = 1
    BOTH = 2
    
class SQUARES(Enum):
    A1 = 21
    A2 = 31
    A3 = 41
    A4 = 51
    A5 = 61
    A6 = 71
    A7 = 81
    A8 = 91
    
    B1 = 22
    B2 = 32
    B3 = 42
    B4 = 52
    B5 = 62
    B6 = 72
    B7 = 82
    B8 = 92
    
    C1 = 23
    C2 = 33
    C3 = 43
    C4 = 53
    C5 = 63
    C6 = 73
    C7 = 83
    C8 = 93
    
    D1 = 24
    D2 = 34
    D3 = 44
    D4 = 54
    D5 = 64
    D6 = 74
    D7 = 84
    D8 = 94
    
    E1 = 25
    E2 = 35
    E3 = 45
    E4 = 55
    E5 = 65
    E6 = 75
    E7 = 85
    E8 = 95
    
    F1 = 26
    F2 = 36
    F3 = 46
    F4 = 56
    F5 = 66
    F6 = 76
    F7 = 86
    F8 = 96
    
    G1 = 27
    G2 = 37
    G3 = 47
    G4 = 57
    G5 = 67
    G6 = 77
    G7 = 87
    G8 = 97
    
    H1 = 28
    H2 = 38
    H3 = 48
    H4 = 58
    H5 = 68
    H6 = 78
    H7 = 88
    H8 = 98
    
    NO_SQ = 99
    OFFBOARD = 100
    
class UNDO:
    def __init__(self):
        self.move = 0 # the move number
        self.castlePerm = 0
        self.enPas = -1
        self.fiftyMove = 0
        self.posKey = 0 #unqiue position key (object of PositionKey Class)
        # castling information
class CASTLING(Enum):
    WKCA = 1 # white king side castling
    WQCA = 2 # white queen side castling
    BKCA = 4
    BQCA = 8
            
# file rank to the square number (120 squares representation)
def FR2SQ(f, r):
    return (21 + f) + (r * 10)

def RAND_64():
    return getrandbits(64)
        
class SEARCHINFO:
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