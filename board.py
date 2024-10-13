from constants import BRD_SQ_NUM, SQUARES, PIECE, COLORS, RANK, FILE, CASTLING, FR2SQ
from globals import Sq64ToSq120, Sq120ToSq64, RanksBrd, FilesBrd
from debug import assert_condition
from hashkeys import GeneratePosKey
from data import PceChar, SideChar, PieceBig, PieceMaj, PieceMin, PieceCol, PieceVal
from bitboards import SetBit

# for printing the square in algebraic form,
def PrSq(sq):
    file = FilesBrd[sq]
    rank = RanksBrd[sq]
    SqStr = "{}{}".format(chr(ord('a') + file), chr(ord('1') + rank))
    
    return SqStr

def ResetBoard(board):
    for i in range(0, BRD_SQ_NUM):
        board.pieces[i] = SQUARES.OFFBOARD.value
    
    # clearing the board, I mean placing every box empty (there's no piece on it)
    for i in range(0, 64):
        board.pieces[Sq64ToSq120[i]] = PIECE.EMPTY.value
        
    for i in range(0, 2): # for white, black
        board.bigPce[i] = 0
        board.majPce[i] = 0
        board.minPce[i] = 0
        board.material[i] = 0
        board.pawns[i] = 0
    
    for i in range(0, 13):
        board.pceNum[i] = 0
        
    board.KingSq[COLORS.WHITE.value] = SQUARES.NO_SQ.value
    board.KingSq[COLORS.BLACK.value] = SQUARES.NO_SQ.value
    
    board.side = COLORS.BOTH.value
    board.enPas = SQUARES.NO_SQ.value
    board.fiftyMove = 0
    
    board.ply = 0
    board.hisPly = 0
    
    board.castlePerm = 0
    board.posKey = 0

def PrintBoard(board):
    print("\nGame Board: \n")
    for rank in range(RANK.R8.value, RANK.R1.value-1, -1):
        print(rank+1, end="   ")
        for file in range(FILE.A.value, FILE.H.value+1):
            sq = FR2SQ(file, rank)
            piece = board.pieces[sq]
            print(f"{PceChar[piece]:3}", end=" ")
        print()
    print()
    print("    ", end="")
    for file in range(FILE.A.value, FILE.H.value + 1):
        print(f"{chr(ord('a') + file):3}", end=" ")
        
    print()
    print(f"Side: {SideChar[board.side]}")
    print(f"En Passant: {PrSq(board.enPas)}")
    
    print(f"Castle: {'K' if board.castlePerm & CASTLING.WKCA.value else '-'} {'Q' if board.castlePerm & CASTLING.WQCA.value else '-'} {'k' if board.castlePerm & CASTLING.BKCA.value else '-'} {'q' if board.castlePerm & CASTLING.BQCA.value else '-'} ")
    
    print(hex(board.posKey))
    

def UpdateListsMaterial(board):
    for index in range(0, BRD_SQ_NUM):
        sq = index
        piece = board.pieces[index]
        if(piece != SQUARES.OFFBOARD.value and piece != PIECE.EMPTY.value):
            colour = PieceCol[piece]
            if(PieceBig[piece]):
                board.bigPce[colour] += 1
            if(PieceMin[piece]):
                board.minPce[colour] += 1
            if(PieceMaj[piece]):
                board.majPce[colour] += 1
            board.material[colour] += PieceVal[piece] # adding the value of material
            
            #Piece List --> pList[wP][pceNum]; example, there's our first white Pawn on e4, pList[wP][0] = E4
            
            # how the following code works, for example we already have 2 white Pawns, so Our pceNum[1] = 2, now If we want to add a white Pawn on E4, we need to do like, pList[wP][2] = E4
            # that's exactly what we are doing
            board.pList[piece][board.pceNum[piece]] = sq #the inner [] represents the number of the piece, I mean if its 1st white pawn, or 2nd or etc....
            board.pceNum[piece] += 1 # incrementing the pceNum
            
            # setting the kingSquare
            if(piece == PIECE.wK.value or piece == PIECE.bK.value):
                board.KingSq[colour] = sq
                
            # setting the pawn bits
            if(piece == PIECE.wP.value):
                board.pawns[COLORS.WHITE.value] = SetBit(board.pawns[COLORS.WHITE.value], Sq120ToSq64[sq] )
                board.pawns[COLORS.BOTH.value] = SetBit(board.pawns[COLORS.BOTH.value], Sq120ToSq64[sq] )
            elif(piece == PIECE.bP.value):
                board.pawns[COLORS.BLACK.value] = SetBit(board.pawns[COLORS.BLACK.value], Sq120ToSq64[sq] )
                board.pawns[COLORS.BOTH.value] = SetBit(board.pawns[COLORS.BOTH.value], Sq120ToSq64[sq] )
                
    
def ParseFen(fen, board):
    assert_condition(fen != None)
    assert_condition(board != None)
    
    fen_parts = fen.split(" ")
    piece, count, sq64, sq120 = 0, 0, 0, 0
    rank = RANK.R8.value
    file = FILE.A.value
    
    ResetBoard(board)
    for char in fen_parts[0]:
        count = 1
        if(char == 'p'):
            piece = PIECE.bP.value
        elif(char == 'r'):
            piece = PIECE.bR.value
        elif(char == 'n'):
            piece = PIECE.bN.value
        elif(char == 'b'):
            piece = PIECE.bB.value
        elif(char == 'k'):
            piece = PIECE.bK.value
        elif(char == 'q'):
            piece = PIECE.bQ.value
        elif(char == 'P'):
            piece = PIECE.wP.value
        elif(char == 'R'):
            piece = PIECE.wR.value
        elif(char == 'N'):
            piece = PIECE.wN.value
        elif(char == 'B'):
            piece = PIECE.wB.value
        elif(char == 'K'):
            piece = PIECE.wK.value
        elif(char == 'Q'):
            piece = PIECE.wQ.value
        
        elif(char == '1' or char == '2' or char == '3' or char == '4' or char == '5' or char == '6' or char == '7' or char == '8'):
            piece = PIECE.EMPTY.value
            count = ord(char) - ord('0')
            
        elif(char == '/' or char == ' '):
            rank -= 1
            file = FILE.A.value
            continue
        else:
            print("Wrong FEN")
            return -1
        for i in range(0, count):
            sq64 = rank * 8 + file # calculating the sqaure64 using file and rank for example. D4 -> 27
            sq120 = Sq64ToSq120[sq64]
            if(piece != PIECE.EMPTY.value):
                board.pieces[sq120] = piece
            file += 1
    
    board.side = COLORS.WHITE.value if fen_parts[1] == 'w' else COLORS.BLACK.value
    for castleCase in fen_parts[2]:
        if(castleCase == "K"):
            board.castlePerm |= CASTLING.WKCA.value
        elif(castleCase == "Q"):
            board.castlePerm |= CASTLING.WQCA.value
        elif(castleCase == "k"):
            board.castlePerm |= CASTLING.BKCA.value
        elif(castleCase == "q"):
            board.castlePerm |= CASTLING.BQCA.value
        else: 
            pass
    assert_condition(board.castlePerm >= 0 and board.castlePerm <= 15)
    print(fen_parts[3])
    
    if(fen_parts[3] != "-"):
        file = ord(fen_parts[3][0]) - ord('a')
        rank = ord(fen_parts[3][1]) - ord('1')
        
        assert_condition(file >= FILE.A.value and file <= FILE.H.value)
        assert_condition(rank >= RANK.R1.value and rank <= RANK.R8.value)
        
        
        board.enPas = FR2SQ(file, rank)
    board.posKey = GeneratePosKey(board) #generating the hashkey
    UpdateListsMaterial(board)
    return 0

    