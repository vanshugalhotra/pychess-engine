from globals import CastleKeys, PieceKeys, SideKey, Sq120ToSq64
from constants import PIECE, COLORS
from debug import assert_condition
from validate import SqOnBoard, PieceValid
from bitboards import ClearBit, SetBit
from data import PieceCol, PieceVal, PieceBig, PieceMaj

def HASH_PCE(pce, sq, board):
    board.posKey ^= PieceKeys[pce][sq]
    
def HASH_CA(board):
    board.posKey ^= CastleKeys[board.castlePerm]

def HASH_SIDE(board):
    board.posKey ^= SideKey
    
def HASH_EP(board):
    board.posKey ^= PieceKeys[PIECE.EMPTY.value][board.enPas]
    
    
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

# function for clearing a piece from the board
def ClearPiece(board, sq):
    assert_condition(SqOnBoard(sq))
    
    pce = board.pieces[sq]
    assert_condition(PieceValid(pce))
    
    HASH_PCE(pce, sq, board) # updating the posKey
    
    col = PieceCol[pce] # getting the color of the piece
    board.pieces[sq] = PIECE.EMPTY.value # making that square empty
    board.material[col] -= PieceVal[pce] # subtracting its value
    
    if(PieceBig[pce]): # if its a non-pawn piece
        board.bigPce[col] -= 1
        if(PieceMaj[pce]): # if its a rook or queen (major pieces)
            board.majPce[col] -= 1
        else: # if its a minor piece (knights , bishops)
            board.minPce[col] -= 1
    else: # if its a pawn
        ClearBit(board.pawns[col], Sq120ToSq64[sq]) # bitboard, sq64
        ClearBit(board.pawns[COLORS.BOTH.value], Sq120ToSq64[sq])


    # removing that particular piece from the pList[][]  
    t_pceIndex = -1
    for index in range(0, board.pceNum[pce]): # looping all the pieces , for example, lets say we want to clear a white pawn on e4, we loop all the whitePawns
        if(board.pList[pce][index] == sq): # we find the index of whitePawn on e4 sqaure particularly
            t_pceIndex = index
            break   
    
    assert_condition(t_pceIndex != -1) # if the t_pceIndex is still not changed, then we have a mismatch on our pieces and pList, we need to debug
    board.pceNum[pce] -= 1 # decrementing pceNum, because we cleared one piece
    # following line , does what is, it places the last piece 's square on the index of the piece we captured
    # ?why because, we decremented the pceNum, instead of shifting all the [piece][] & squares, we just move the last one.
    board.pList[pce][t_pceIndex] = board.pList[pce][board.pceNum[pce]]

def AddPiece(board, sq, pce):
    assert_condition(PieceValid(pce))
    assert_condition(SqOnBoard(sq))
    
    col = PieceCol[pce]
    HASH_PCE(pce, sq, board)
    
    board.pieces[sq] = pce
    
    if(PieceBig[pce]):
        board.bigPce[col] += 1
        if(PieceMaj[pce]):
            board.majPce[col] += 1
        else:
            board.minPce[col] += 1
    else: 
        SetBit(board.pawns[col], Sq120ToSq64[sq])
        SetBit(board.pawns[COLORS.BOTH.value], Sq120ToSq64[sq])
        
    board.material[col] += PieceVal[pce] #updating the material value
    board.pList[pce][board.pceNum[pce]] = sq # setting the pce on pList
    board.pceNum[pce] += 1
    
def MovePiece(fromSq, toSq, board):
    assert_condition(SqOnBoard(fromSq))
    assert_condition(SqOnBoard(toSq))
    
    pce = board.pieces[fromSq]
    col = PieceCol[pce]
    
    t_PieceIndex = False
    
    HASH_PCE(pce, fromSq, board)
    board.pieces[fromSq] = PIECE.EMPTY.value
    
    HASH_PCE(pce,toSq, board)
    board.pieces[toSq] = pce
    
    if(not PieceBig[pce]): # if its a pawn
        ClearBit(board.pawns[col], Sq120ToSq64[fromSq])
        ClearBit(board.pawns[COLORS.BOTH.value], Sq120ToSq64[fromSq])
        SetBit(board.pawns[col], Sq120ToSq64[toSq])
        SetBit(board.pawns[COLORS.BOTH.value], Sq120ToSq64[toSq])
        
    for index in range(0, board.pceNum[pce]):
        if(board.pList[pce][index] == fromSq):
            board.pList[pce][index] = toSq
            t_PieceIndex = True
            break
    
    assert_condition(t_PieceIndex)
    
    