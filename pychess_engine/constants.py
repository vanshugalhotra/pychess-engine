from collections import namedtuple

BRD_SQ_NUM = 120
MAXGAMEMOVES = 2048
MAXPOSITIONMOVES = 256
MAXDEPTH = 64

Piece = namedtuple("Piece", ['EMPTY', 'wP', 'wN', 'wB','wR', 'wQ', 'wK', 'bP', 'bN', 'bB', 'bR', 'bQ', 'bK'])
Pieces = Piece(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

File = namedtuple("File", ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', "NONE"])
Files = File(0, 1, 2, 3, 4, 5, 6, 7, 8)

Rank = namedtuple("Rank", ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'RNONE'])
Ranks = Rank(0, 1, 2, 3, 4, 5, 6, 7, 8)

Color = namedtuple("Color", ["WHITE", "BLACK", "BOTH"])
Colors = Color(0, 1, 2)    

Square = namedtuple("Square", [
    "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8",
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8",
    "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8",
    "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8",
    "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8",
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8",
    "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8",
    "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8",
    "NO_SQ", "OFFBOARD"
])

Squares = Square(
    21, 31, 41, 51, 61, 71, 81, 91,
    22, 32, 42, 52, 62, 72, 82, 92,
    23, 33, 43, 53, 63, 73, 83, 93,
    24, 34, 44, 54, 64, 74, 84, 94,
    25, 35, 45, 55, 65, 75, 85, 95,
    26, 36, 46, 56, 66, 76, 86, 96,
    27, 37, 47, 57, 67, 77, 87, 97,
    28, 38, 48, 58, 68, 78, 88, 98,
    99, 100
)

Castle = namedtuple("Castle", ['WKCA', 'WQCA', 'BKCA', 'BQCA'])
Castling = Castle(1, 2, 4, 8)
