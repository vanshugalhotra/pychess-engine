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

# move flags, to retrieve information from the move
MFLAGEP = 0x40000 # to check if the capture was EnPassant or not
MFLAGPS = 0x80000 # to check if it was a pawn move
MFLAGCA = 0x1000000 # to check if it was a castle move
MFLAGCAP = 0x7C000 # to check if there occured any capture at all
MFLAGPROM = 0xF00000 # to check if there occured any promotion of pawn

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
        self.posKey = 0 #unqiue position key
        
class Board:
    def __init__(self):
        # 120 squares to represent the board
        self.pieces = [0] * BRD_SQ_NUM

        # represent the pawns of both sides (0 for white, 1 for black, 2 for both)
        self.pawns = [0] * 3  

        # Position of kings (0 for white, 1 for black)
        self.KingSq = [0] * 2

        # Side to move (0 for white, 1 for black)
        self.side = 0

        # En passant square (-1 means no en passant square)
        self.enPas = -1

        # Fifty-move rule counter
        self.fiftyMove = 0

        # Ply (depth of search in current game)
        self.ply = 0

        # history of half moves in game
        self.hisPly = 0
        
        # castle permission
        self.castlePerm = 0

        # Unique Position key for each Position
        self.posKey = 0

        # 
        self.pceNum = [0] * 13  # Total Number of pieces (Like pceNum[1] = 6 means we have 6 white pawns)

        # Number of non-pawn big pieces (Queens, rooks, bishops, knights)
        self.bigPce = [0] * 2  # 0 for white, 1 for black

        # Number of major pieces (Queens and Rooks)
        self.majPce = [0] * 2  # 0 for white, 1 for black 

        # Number of minor pieces (Bishops and Knights)
        self.minPce = [0] * 2  # 0 for white, 1 for black
        
        # Material Value of Pieces  
        self.material = [0] * 2
        
        # Declare an array of UNDO class instances
        self.history = [UNDO() for _ in range(MAXGAMEMOVES)]
        
        #piece list, pList[wN][0] = E1; adds a white knight on e1
        self.pList = [[0 for _ in range(10)] for _ in range(13)] 
        
        #declaring pvTable
        self.PvTable = PVTABLE()
        self.PvArray = [0] * MAXDEPTH
        
        # !explanation needed
        #needed for move ordering
        # searchHistory[13][120] indexed by piece type and board square, everytime a move improves by alpha we reset all the values stored in this array to 0, 
        # when a piece beats alpha for that piece type and TOSQ we increment by 1
        self.searchHistory = [[0 for _ in range(BRD_SQ_NUM)] for _ in range(13)]
        
        # searchKillers[2][MAXDEPTH], stores 2 recent moves which caused the beta cutoff which aren't captures
        self.searchKillers = [[0 for _ in range(MAXDEPTH)] for _ in range(2)]
        

# castling information
class CASTLING(Enum):
    WKCA = 1 # white king side castling
    WQCA = 2 # white queen side castling
    BKCA = 4
    BQCA = 8
    
class MOVE:
    def __init__(self):
        self.move = 0
        # move represents the following information in 25 bits
        # FROM (square)(21 - 98)  - 7 bits
        # TO (square) - 7 bits
        # Captured Piece (0 - 12) - 4 bits
        # EnPas Capture? (0 - 1) - 1 bit
        # Pawn Start ? (0 - 1) - 1 bit
        # Promoted Piece (0 - 12) - 4 bits
        # castle move? (0 - 1) - 1 bit
        self.score = 0
        
# file rank to the square number (120 squares representation)
def FR2SQ(f, r):
    return (21 + f) + (r * 10)

def RAND_64():
    return getrandbits(64)

# functions to retrieve information from the move
def FROMSQ(move):
    return move & 0x7F #extracting the last 7 bits from the move number

def TOSQ(move):
    return (move >> 7) & 0x7F # first right shift the bits to 7 and then extract the last 7 bits which represents now TO Square

def CAPTURED(move):
    return (move >> 14) & 0xF # 4 bits

def PROMOTED(move):
    return (move >> 20) & 0xF

class MOVELIST:
    def __init__(self):
        self.moves = [MOVE() for _ in range(MAXPOSITIONMOVES)]
        self.count = 0
        
class PVENTRY:
    def __init__(self):
        self.posKey = 0
        self.move = 0

class PVTABLE:
    def __init__(self):
        self.numEntries = 0
        self.pTable = [] # to store the entry of PVENTRY
        
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