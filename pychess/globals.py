from pychess.constants import BRD_SQ_NUM, Pieces, Colors, Squares

Sq120ToSq64 = [65] * BRD_SQ_NUM # initially every box is 65 (representing offboard)
Sq64ToSq120 = [120] * 64 # initially every box is 120 doesn't mean anything we can put any value

setMask = [0] * 64
clearMask = [0] * 64

FilesBrd = [Squares.OFFBOARD] * BRD_SQ_NUM
RanksBrd = [Squares.OFFBOARD] * BRD_SQ_NUM


PceChar = ".PNBRQKpnbrqk"
SideChar = "wb-"
RankChar = "12345678"
FileChar = "abcdefgh"

CastlePerm = [
    15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
    15, 13, 15, 15, 15, 12, 15, 15, 14, 15,
    15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
    15,  7, 15, 15, 15,  3, 15, 15, 11, 15,
    15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15, 15, 15,   
]

PieceBig = [False, False, True, True, True,True, True, False,True, True, True, True, True]
PieceMaj = [False, False, False, False, True, True, True, False, False, False,True, True, True]
PieceMin = [False, False, True, True, False, False, False, False, True, True,False, False, False]
PieceVal = [0, 100, 325,325,  550, 1000, 50000, 100, 325, 325, 550, 1000, 50000]
PieceCol = [Colors.BOTH, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK]

PiecePawn = [False, True, False, False, False, False, False, True, False, False, False, False, False] # is Piece a Pawn ?
PieceKnight = [False, False, True, False, False, False, False, False, True, False, False, False, False] # is Piece a Knight ?
PieceKing = [False, False, False, False, False, False, True, False, False, False, False, False, True] # is Piece a King ?
PieceRookQueen = [False, False, False, False, True, True, False, False, False, False, True, True, False] # is Piece a Rook or a Queen ?
PieceBishopQueen = [False, False, False, True, False, True, False, False, False, True, False, True, False] # is Piece a Bishop or a Queen ?

PieceSlides = [False, False, False, True, True, True, False, False, False, True, True, True, False]

LoopSlidePce = [Pieces.wB, Pieces.wR, Pieces.wQ, 0, Pieces.bB, Pieces.bR, Pieces.bQ, 0] # initially, lets say WHITE is generating moves then it will start from index 0 and loop till value is 0, means till number is 0, we generate moves for sliding pieces

LoopNonSlidePce = [Pieces.wN, Pieces.wK, 0, Pieces.bN, Pieces.bK, 0]

LoopSlideIndex = [0, 4] # IF WHITE starts - 0, if BLACK - 4.
LoopNonSlideIndex = [0, 3]

PceDir = [ # directions for each piece
    [0 ,0, 0, 0, 0, 0, 0], # 0 - empty
    [0 ,0, 0, 0, 0, 0, 0], # 1 - white Pawn
    [-8, -19, -21, -12, 8, 19, 21, 12], # 2 - white Knight
    [-9, -11, 11, 9, 0, 0, 0, 0], # 3 - white bishop
    [-1, -10, 1, 10, 0, 0, 0, 0], # 4 - white rook
    [-1, -10, 1, 10, -9, -11, 11, 9], # 5 - white queen
    [-1 , -10, 1, 10, -9, -11, 11, 9], # 6 - white king
    [0, 0, 0, 0, 0, 0 , 0], # 7 - black pawns
    [-8, -19, -21, -12, 8, 19, 21, 12], # 8 - black knight
    [-9, -11, 11, 9, 0, 0, 0, 0], # 9 - black bishop
    [-1, -10, 1, 10, 0, 0, 0, 0], # 10 - black rook
    [-1, -10, 1, 10, -9, -11, 11, 9], # 11 - black queen
    [-1, -10, 1, 10, -9, -11, 11, 9]  # 12 - black king
]

NumDir = [0, 0, 8, 4, 4, 8, 8, 0, 8, 4, 4, 8, 8] # no of directions, for example, for rook we have 4

"""
PV Move
Cap -> MvvLVA (Most valuable victim Least valuable attacker)
Killers (beta cutoffs)
HistoryScore

[Vic][Att] highest score is P X Q (pawn takes queen) and lowest is queen takes pawn
    P x Q
    N x Q
    B x Q
    R x Q
    .....
    P x R
    B
    N
    P
    
Victim Q -> 500
Victim R -> 400 

"""

VictimScore = [0, 100, 200, 300, 400, 500, 600, 100, 200, 300, 400, 500, 600]

# the following array also covers, white pawn takes white pawn and also similar illegal captures but we will deal with them later
MvvLvaScores = [[VictimScore[victim] + 6 - (VictimScore[attacker] // 100) for attacker in range(0, Pieces.bK + 1)] for victim in range(0, Pieces.bK + 1)]


# basic evaluation values, like this says pawn on e5 is worth a 20 value than a pawn on a a5
# After the computer plays many games, these values are adjusted based upon how well the pieces actually preformed on the various squares.
# Beginners are taught that the more centralized piece is better placed, and the computer is taught this basic rules via these tables.
PawnTable = [
0	,	0	,	0	,	0	,	0	,	0	,	0	,	0	,
10	,	10	,	0	,	-10	,	-10	,	0	,	10	,	10	,
5	,	0	,	0	,	5	,	5	,	0	,	0	,	5	,
0	,	0	,	10	,	20	,	20	,	10	,	0	,	0	,
5	,	5	,	5	,	10	,	10	,	5	,	5	,	5	,
10	,	10	,	10	,	20	,	20	,	10	,	10	,	10	,
20	,	20	,	20	,	30	,	30	,	20	,	20	,	20	,
0	,	0	,	0	,	0	,	0	,	0	,	0	,	0	
]

# evaluation values for knight, Knights have more squares available when on the center  squares(8) than in the corner(2), therefore the central square have a higher value. 
KnightTable = [
0	,	-10	,	0	,	0	,	0	,	0	,	-10	,	0	,
0	,	0	,	0	,	5	,	5	,	0	,	0	,	0	,
0	,	0	,	10	,	10	,	10	,	10	,	0	,	0	,
0	,	0	,	10	,	20	,	20	,	10	,	5	,	0	,
5	,	10	,	15	,	20	,	20	,	15	,	10	,	5	,
5	,	10	,	10	,	20	,	20	,	10	,	10	,	5	,
0	,	0	,	5	,	10	,	10	,	5	,	0	,	0	,
0	,	0	,	0	,	0	,	0	,	0	,	0	,	0		
]

# for bishops
BishopTable = [
0	,	0	,	-10	,	0	,	0	,	-10	,	0	,	0	,
0	,	0	,	0	,	10	,	10	,	0	,	0	,	0	,
0	,	0	,	10	,	15	,	15	,	10	,	0	,	0	,
0	,	10	,	15	,	20	,	20	,	15	,	10	,	0	,
0	,	10	,	15	,	20	,	20	,	15	,	10	,	0	,
0	,	0	,	10	,	15	,	15	,	10	,	0	,	0	,
0	,	0	,	0	,	10	,	10	,	0	,	0	,	0	,
0	,	0	,	0	,	0	,	0	,	0	,	0	,	0	
]

# for rooks
RookTable = [
0	,	0	,	5	,	10	,	10	,	5	,	0	,	0	,
0	,	0	,	5	,	10	,	10	,	5	,	0	,	0	,
0	,	0	,	5	,	10	,	10	,	5	,	0	,	0	,
0	,	0	,	5	,	10	,	10	,	5	,	0	,	0	,
0	,	0	,	5	,	10	,	10	,	5	,	0	,	0	,
0	,	0	,	5	,	10	,	10	,	5	,	0	,	0	,
25	,	25	,	25	,	25	,	25	,	25	,	25	,	25	,
0	,	0	,	5	,	10	,	10	,	5	,	0	,	0		
]

# the mirror array is used to get the squares for black
# for example, if we dealing with a2 than equivalent for black is a7 which is index 48
Mirror64 = [
56	,	57	,	58	,	59	,	60	,	61	,	62	,	63	,
48	,	49	,	50	,	51	,	52	,	53	,	54	,	55	,
40	,	41	,	42	,	43	,	44	,	45	,	46	,	47	,
32	,	33	,	34	,	35	,	36	,	37	,	38	,	39	,
24	,	25	,	26	,	27	,	28	,	29	,	30	,	31	,
16	,	17	,	18	,	19	,	20	,	21	,	22	,	23	,
8	,	9	,	10	,	11	,	12	,	13	,	14	,	15	,
0	,	1	,	2	,	3	,	4	,	5	,	6	,	7
]
