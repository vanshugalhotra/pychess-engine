from globals import CastleKeys, PieceKeys, SideKey, Sq120ToSq64, RanksBrd
from constants import PIECE, COLORS, FROMSQ, TOSQ, MFLAGEP, MFLAGCA, SQUARES, CAPTURED, MFLAGPS, RANK, PROMOTED
from debug import assert_condition
from validate import SqOnBoard, PieceValid, SideValid
from bitboards import ClearBit, SetBit
from data import PieceCol, PieceVal, PieceBig, PieceMaj, PiecePawn, PieceKing
from board import CheckBoard
from attack import SqAttacked

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
        board.pawns[col] = ClearBit(board.pawns[col], Sq120ToSq64[sq]) # bitboard, sq64
        board.pawns[COLORS.BOTH.value] = ClearBit(board.pawns[COLORS.BOTH.value], Sq120ToSq64[sq])


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
        board.pawns[col] = SetBit(board.pawns[col], Sq120ToSq64[sq])
        board.pawns[COLORS.BOTH.value] = SetBit(board.pawns[COLORS.BOTH.value], Sq120ToSq64[sq])
        
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
        board.pawns[col] = ClearBit(board.pawns[col], Sq120ToSq64[fromSq])
        board.pawns[COLORS.BOTH.value] = ClearBit(board.pawns[COLORS.BOTH.value], Sq120ToSq64[fromSq])
        board.pawns[col] = SetBit(board.pawns[col], Sq120ToSq64[toSq])
        board.pawns[COLORS.BOTH.value] = SetBit(board.pawns[COLORS.BOTH.value], Sq120ToSq64[toSq])
        
    for index in range(0, board.pceNum[pce]):
        if(board.pList[pce][index] == fromSq):
            board.pList[pce][index] = toSq
            t_PieceIndex = True
            break
    
    assert_condition(t_PieceIndex)
    
def TakeMove(board): # taking the move back, due to some reasons (maybe it was an illegal move)
    assert_condition(CheckBoard(board))
    
    # resetting the counters
    board.hisPly -= 1
    board.ply -= 1
    
    move = board.history[board.hisPly].move # getting the move from the history
    fromSq = FROMSQ(move)
    toSq = TOSQ(move) 
    
    assert_condition(SqOnBoard(fromSq))
    assert_condition(SqOnBoard(toSq))
    
    if(board.enPas != SQUARES.NO_SQ.value):
        HASH_EP(board)
    HASH_CA(board) # hashing out the current castle Perm
    
    board.castlePerm = board.history[board.hisPly].castlePerm # retreiving back the previous castlePerm
    board.fiftyMove = board.history[board.hisPly].fiftyMove
    board.enPas = board.history[board.hisPly].enPas
    
    if(board.enPas != SQUARES.NO_SQ.value):
        HASH_EP(board)
    HASH_CA(board) # hashing in the new castle permission
    
    board.side ^= 1 #changing back the side
    HASH_SIDE(board)
    
    if(move & MFLAGEP): # if it was an enPas capture, then we add back the pieces
        if(board.side == COLORS.WHITE.value):
            AddPiece(board, toSq-10, PIECE.bP.value)
        else:
            AddPiece(board, toSq+10, PIECE.wP.value)
            
    elif(move & MFLAGCA): # if it was a castle move
        if(toSq == SQUARES.C1.value):
            MovePiece(SQUARES.D1.value, SQUARES.A1.value, board) # moving back the rook
        elif(toSq == SQUARES.C8.value):
            MovePiece(SQUARES.D8.value, SQUARES.A8.value, board) # moving back the rook
        elif(toSq == SQUARES.G1.value):
            MovePiece(SQUARES.F1.value, SQUARES.H1.value, board) # moving back the rook
        elif(toSq == SQUARES.G8.value):
            MovePiece(SQUARES.F8.value, SQUARES.H8.value, board) # moving back the rook
        else:
            assert_condition(False)
            
    # moving back the piece
    MovePiece(toSq, fromSq, board)
    
    if(PieceKing[board.pieces[fromSq]]):
        board.KingSq[board.side] = fromSq # moving back the king
        
    captured = CAPTURED(move)
    if(captured != PIECE.EMPTY.value):
        assert_condition(PieceValid(captured))
        AddPiece(board, toSq, captured) # adding back the captured piece
        
    prPce = PROMOTED(move)
    if(prPce != PIECE.EMPTY.value): #  ! explanation is needed
        assert_condition(PieceValid(prPce) and not PiecePawn[prPce])
        ClearPiece(board, fromSq)
        toAdd = PIECE.wP.value if PieceCol[prPce] == COLORS.WHITE.value else PIECE.bP.value
        AddPiece(board, fromSq, toAdd)
    
    assert_condition(CheckBoard(board))
    
    
def MakeMove(board, move): # it returns 0 (meaning illegal move) when? when after making the move, the king of the side which made the move is in CHECK.
    assert_condition(CheckBoard(board))
    fromSq = FROMSQ(move)
    toSq = TOSQ(move)
    side = board.side
    
    assert_condition(SqOnBoard(fromSq))
    assert_condition(SqOnBoard(toSq))
    assert_condition(SideValid(side))
    assert_condition(PieceValid(board.pieces[fromSq]))
    
    # storing the move in history, before changing any posKey, we store the posKey in history
    board.history[board.hisPly].posKey = board.posKey # history array contains the objects of class UNDO()
    
    if(move & MFLAGEP): # if its an enpassant capture
        if(side == COLORS.WHITE.value):
            ClearPiece(board, toSq-10) # capturing the black pawn
        else:
            ClearPiece(board, toSq+10) # capturing the white pawn
    elif(move & MFLAGCA): # if its an castle MOVE
        if(toSq == SQUARES.C1.value):
            MovePiece(SQUARES.A1.value, SQUARES.D1.value, board)
        elif(toSq == SQUARES.C8.value):
            MovePiece(SQUARES.A8.value, SQUARES.D8.value, board)
        elif(toSq == SQUARES.G1.value): # white king side castling
            MovePiece(SQUARES.H1.value, SQUARES.F1.value, board) # moving the rook from h1 -> f1
        elif(toSq == SQUARES.G8.value):
            MovePiece(SQUARES.H8.value, SQUARES.F8.value, board)
        else:
            assert_condition(False)
            
    if(board.enPas != SQUARES.NO_SQ.value):
        HASH_EP(board)
        
    HASH_CA(board) # hashing out the castle permission
    
    board.history[board.hisPly].move = move
    board.history[board.hisPly].fiftyMove = board.fiftyMove
    board.history[board.hisPly].enPas = board.enPas
    board.history[board.hisPly].castlePerm = board.castlePerm
    
    board.castlePerm &= CastlePerm[fromSq] # if king or rook has moved
    board.castlePerm &= CastlePerm[toSq] # if rook or king has moved
    board.enPas = SQUARES.NO_SQ.value
    
    HASH_CA(board) # hashing in the new castle permission
    
    captured = CAPTURED(move)
    board.fiftyMove += 1
    
    if(captured != PIECE.EMPTY.value):
        assert_condition(PieceValid(captured))
        ClearPiece(board, toSq) # first we capture on the toSq, then we move
        board.fiftyMove = 0 # if a capture is made, then fifty move is set to 0
    
    board.hisPly += 1
    board.ply += 1
    
    # setting up the enPas sqaure
    if(PiecePawn[board.pieces[fromSq]]): # if the piece on fromSq was a pawn
        board.fiftyMove = 0 # if its a pawn move, reset the counter
        if(move & MFLAGPS): # if it was a pawn start move
            if(side == COLORS.WHITE.value):
                board.enPas = fromSq + 10
                assert_condition(RanksBrd[board.enPas] == RANK.R3.value)
            else:
                board.enPas = fromSq - 10
                assert_condition(RanksBrd[board.enPas] == RANK.R6.value)
            HASH_EP(board) # hashing in the new enPas
    
    # finally moving the piece on the board
    MovePiece(fromSq, toSq, board)
    
    # checking for promotions
    prPce = PROMOTED(move) 
    if(prPce != PIECE.EMPTY.value):
        assert_condition(PieceValid(prPce) and not PiecePawn[prPce])
        
        # ! explanation needed
        ClearPiece(board, toSq) # clearing the toSq
        AddPiece(board, toSq, prPce) # adding the promoted piece on the toSq
        
    # updating the kingsquare
    if(PieceKing[board.pieces[toSq]]):
        board.KingSq[board.side] = toSq
    
    board.side ^= 1 # changing the side
    HASH_SIDE(board) 
    
    assert_condition(CheckBoard(board))
    
    if(SqAttacked(board.KingSq[side], board.side, board)): # side is the side which made the move, board.side now is now the opposite side, so we check if after making the move, the opposite side is attacking the KingSq, means king is in check, then its an illegal move
        TakeMove(board)   # take back the move
        return False
    
    return True
    
    