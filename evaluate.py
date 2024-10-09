from constants import COLORS, PIECE
from debug import assert_condition
from validate import SqOnBoard
from globals import Sq120ToSq64

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


# returns an integer - which says the evaluation score of the position from sidetoMovePOV
def EvalPosition(board):
    pce = 0
    score = board.material[COLORS.WHITE.value] - board.material[COLORS.BLACK.value]
    
    pce=PIECE.wP.value
    for pceNum in range(0, board.pceNum[pce]): # traversing all the white pawns
        sq = board.pList[pce][pceNum] # getting the 120 based square on which the piece is
        assert_condition(SqOnBoard(sq))
        score += PawnTable[Sq120ToSq64[sq]]
    
    pce=PIECE.bP.value
    for pceNum in range(0, board.pceNum[pce]): # traversing all the black pawns
        sq = board.pList[pce][pceNum] # getting the 120 based square on which the piece is
        assert_condition(SqOnBoard(sq))
        score -= PawnTable[Mirror64[Sq120ToSq64[sq]]] # mirroring the square for black
        
    pce=PIECE.wN.value
    for pceNum in range(0, board.pceNum[pce]): # traversing all the white knights
        sq = board.pList[pce][pceNum] # getting the 120 based square on which the piece is
        assert_condition(SqOnBoard(sq))
        score += KnightTable[Sq120ToSq64[sq]]
    
    pce=PIECE.bN.value
    for pceNum in range(0, board.pceNum[pce]): # traversing all the black knights
        sq = board.pList[pce][pceNum] # getting the 120 based square on which the piece is
        assert_condition(SqOnBoard(sq))
        score -= KnightTable[Mirror64[Sq120ToSq64[sq]]] # mirroring the square for black
        
    pce=PIECE.wB.value
    for pceNum in range(0, board.pceNum[pce]): # traversing all the white bishops
        sq = board.pList[pce][pceNum] # getting the 120 based square on which the piece is
        assert_condition(SqOnBoard(sq))
        score += BishopTable[Sq120ToSq64[sq]]
    
    pce=PIECE.bB.value
    for pceNum in range(0, board.pceNum[pce]): # traversing all the black bishops
        sq = board.pList[pce][pceNum] # getting the 120 based square on which the piece is
        assert_condition(SqOnBoard(sq))
        score -= BishopTable[Mirror64[Sq120ToSq64[sq]]] # mirroring the square for black
        
    pce=PIECE.wR.value
    for pceNum in range(0, board.pceNum[pce]): # traversing all the white rooks
        sq = board.pList[pce][pceNum] # getting the 120 based square on which the piece is
        assert_condition(SqOnBoard(sq))
        score += RookTable[Sq120ToSq64[sq]]
    
    pce=PIECE.bR.value
    for pceNum in range(0, board.pceNum[pce]): # traversing all the black rooks
        sq = board.pList[pce][pceNum] # getting the 120 based square on which the piece is
        assert_condition(SqOnBoard(sq))
        score -= RookTable[Mirror64[Sq120ToSq64[sq]]] # mirroring the square for black
        
    if(board.side == COLORS.WHITE.value):
        return score
    else:
        return -score # negating the score for black (because we are calculating score based on white, lets say black's score is better than our score value will be -ve because score = whiteMaterial - blackMaterial and later on we are subtracting for black and adding for white)
    
    
    return 0