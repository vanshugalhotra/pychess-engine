from constants import *
from globals import Sq64ToSq120, Sq120ToSq64, RanksBrd
from debug import assert_condition, DEBUG
from hashkeys import PositionKey
from globals import *
from bitboards import SetBit, PopBit, CountBits, ClearBit
from validate import SqOnBoard, PieceValid, SideValid
from attack import is_sqaure_attacked
from move import MOVE, MOVELIST
from pvtable import PVTABLE
from helper import FR2SQ

class Board:
    """
    Representing the game board for a chess game. Handles
    the initialization of the board, managing the pieces, and checking the state 
    of the game. It includes methods for piece movement, validation, and board display.

    Attributes:
        pieces (list): A list representing on which square we have which piece indexed by squares (0 - 119)
        pawns(list): list of pawn bitboards indexed by colors (0 - `WHITE`, 1 -`BLACK` , 2 - `BOTH` )
        king_square(list): representing sqaure on which king is placed indexed by colors `WHITE` & `BLACK`
        side(int): Side to move (0 - `WHITE`, 1 - `BLACK`)
        enPas(int): EnPassant Square
        fiftyMove(int): Fifty-move rule counter
        ply(int): depth of search in current game (number of half moves)
        hisPly(int): History of half moves in game
        castlePerm(int): Castle Permission (`15<1111>` - All Castles Possible, `14<1110> - White can't castle King Side`, ...)
        posKey(PositionKey): Unique Position Key for each position
        pceNum(list): Total Number of a particular piece indexed by piece number (0 - `EMPTY`, 1 - `wP`, ... 12 - `bK`)
        bigPce(list): Number big pieces i.e Non-Pawn pieces (Queens, rooks, bishops, knights) indexed by colors (0 - `WHITE` , 1 - `BLACK`)
        majPce(list): Number of major pieces (Queens, Rooks) indexed by colors (0 - `WHITE` , 1 - `BLACK`)
        minPce(list): Number of minor pieces (Knights, Bishops) indexed by colors (0 - `WHITE` , 1 - `BLACK`)
        material(list): Total material value for each side indexed by colors (0 - `WHITE` , 1 - `BLACK`)
        history(list of UNDO()): Storing Past Positions
        pList(list of list): piece list specifying a square of a particular piece indexed by [pieceType][kth piece]example, pList[wN][0] = E1; adds a white knight on e1
        PvTable(PVTABLE): principal variation table
        PvArray(list): principal variation array
        searchHistory(list of MOVE()): for heuristics, indexed by [pieceType][BoardSquare]
        searchKillers(list of MOVE()): for heuristics, stores 2 recent moves which caused the beta cutoff which aren't captures
            
    """
    def __init__(self):
        self.pieces = [0] * BRD_SQ_NUM
        self.pawns = [0] * 3  # pawn bitboards
        self.king_square = [0] * 2 # position of king (0 - WHITE, 1 - BLACK)
        self.side = 0 # Side to move (0 for white, 1 for black)
        self.enPas = -1 # En passant square (-1 means no en passant square)
        self.fiftyMove = 0
        self.ply = 0 # Ply (depth of search in current game)
        self.hisPly = 0 # history of half moves in game
        self.castlePerm = 0

        self.posKey = PositionKey() # Unique Position key for each Position

        self.pceNum = [0] * 13  # Total Number of pieces (Like pceNum[1] = 6 means we have 6 white pawns)
        self.bigPce = [0] * 2  # Number of non-pawn big pieces (Queens, rooks, bishops, knights)
        self.majPce = [0] * 2  # Number of major pieces (Queens and Rooks)
        self.minPce = [0] * 2  # Number of minor pieces (Bishops and Knights)
        
        self.material = [0] * 2 # Material Value of Pieces  
        
        self.history = [UNDO() for _ in range(MAXGAMEMOVES)]
        self.pList = [[0 for _ in range(10)] for _ in range(13)] #piece list, pList[wN][0] = E1; adds a white knight on e1
        
        self.PvTable = PVTABLE()
        self.PvArray = [0] * MAXDEPTH
        
        #needed for move ordering
        # searchHistory[13][120] indexed by piece type and board square, everytime a move improves by alpha we reset all the values stored in this array to 0, 
        # when a piece beats alpha for that piece type and TOSQ we increment by 1
        self.searchHistory = [[MOVE() for _ in range(BRD_SQ_NUM)] for _ in range(13)] 
        
        self.searchKillers = [[MOVE() for _ in range(MAXDEPTH)] for _ in range(2)] # searchKillers[2][MAXDEPTH], stores 2 recent moves which caused the beta cutoff which aren't captures
        
    def reset_board(self):
        """
        Resetting the board to initial state
        
        """
        for i in range(0, BRD_SQ_NUM):
            self.pieces[i] = Squares.OFFBOARD
    
        # clearing the board, I mean placing every box empty (there's no piece on it)
        for i in range(0, 64):
            self.pieces[Sq64ToSq120[i]] = Pieces.EMPTY
            
        for i in range(0, 2): # for white, black
            self.bigPce[i] = 0
            self.majPce[i] = 0
            self.minPce[i] = 0
            self.material[i] = 0
            self.pawns[i] = 0
        self.pawns[2] = 0
        
        for i in range(0, 13):
            self.pceNum[i] = 0
            
        self.king_square[Colors.WHITE] = Squares.NO_SQ
        self.king_square[Colors.BLACK] = Squares.NO_SQ
        
        self.side = Colors.BOTH
        self.enPas = Squares.NO_SQ
        self.fiftyMove = 0
        
        self.ply = 0
        self.hisPly = 0
        
        self.castlePerm = 0
        self.posKey = PositionKey()
        
        self.legal_moves = MOVELIST()

    def print_board(self):
        """
        Printing the board
        
        """
        print("\nGame Board: \n")
        for rank in range(Ranks.R8, Ranks.R1-1, -1):
            print(rank+1, end="   ")
            for file in range(Files.A, Files.H+1):
                sq = FR2SQ(file, rank)
                piece = self.pieces[sq]
                print(f"{PceChar[piece]:3}", end=" ")
            print()
        print()
        print("    ", end="")
        for file in range(Files.A, Files.H + 1):
            print(f"{chr(ord('a') + file):3}", end=" ")
            
        print()
        print(f"Side: {SideChar[self.side]}")
        print(f"En Passant: {(self.enPas)}")
        
        print(f"Castle: {'K' if self.castlePerm & Castling.WKCA else '-'} {'Q' if self.castlePerm & Castling.WQCA else '-'} {'k' if self.castlePerm & Castling.BKCA else '-'} {'q' if self.castlePerm & Castling.BQCA else '-'} ")
        
        print(hex(self.posKey.key))

    def update_list_material(self):
        """
        Updating the list material
        
        """
        for index in range(0, BRD_SQ_NUM):
            sq = index
            piece = self.pieces[index]
            if(piece != Squares.OFFBOARD and piece != Pieces.EMPTY):
                colour = PieceCol[piece]
                if(PieceBig[piece]):
                    self.bigPce[colour] += 1
                if(PieceMin[piece]):
                    self.minPce[colour] += 1
                if(PieceMaj[piece]):
                    self.majPce[colour] += 1
                self.material[colour] += PieceVal[piece] # adding the value of material
                
                #Piece List --> pList[wP][pceNum]; example, there's our first white Pawn on e4, pList[wP][0] = E4
                
                # how the following code works, for example we already have 2 white Pawns, so Our pceNum[1] = 2, now If we want to add a white Pawn on E4, we need to do like, pList[wP][2] = E4
                # that's exactly what we are doing
                self.pList[piece][self.pceNum[piece]] = sq #the inner [] represents the number of the piece, I mean if its 1st white pawn, or 2nd or etc....
                self.pceNum[piece] += 1 # incrementing the pceNum
                
                # setting the king_squareuare
                if(piece == Pieces.wK or piece == Pieces.bK):
                    self.king_square[colour] = sq
                    
                # setting the pawn bits
                if(piece == Pieces.wP):
                    self.pawns[Colors.WHITE] = SetBit(self.pawns[Colors.WHITE], Sq120ToSq64[sq] )
                    self.pawns[Colors.BOTH] = SetBit(self.pawns[Colors.BOTH], Sq120ToSq64[sq] )
                elif(piece == Pieces.bP):
                    self.pawns[Colors.BLACK] = SetBit(self.pawns[Colors.BLACK], Sq120ToSq64[sq] )
                    self.pawns[Colors.BOTH] = SetBit(self.pawns[Colors.BOTH], Sq120ToSq64[sq] )

    def parse_fen(self, fen) -> bool:
        if (not fen):
            return False

        fen_parts = fen.split(" ")
        piece, count, sq64, sq120 = 0, 0, 0, 0
        rank = Ranks.R8
        file = Files.A
        
        self.reset_board()
        for char in fen_parts[0]:
            count = 1
            if(char == 'p'):
                piece = Pieces.bP
            elif(char == 'r'):
                piece = Pieces.bR
            elif(char == 'n'):
                piece = Pieces.bN
            elif(char == 'b'):
                piece = Pieces.bB
            elif(char == 'k'):
                piece = Pieces.bK
            elif(char == 'q'):
                piece = Pieces.bQ
            elif(char == 'P'):
                piece = Pieces.wP
            elif(char == 'R'):
                piece = Pieces.wR
            elif(char == 'N'):
                piece = Pieces.wN
            elif(char == 'B'):
                piece = Pieces.wB
            elif(char == 'K'):
                piece = Pieces.wK
            elif(char == 'Q'):
                piece = Pieces.wQ
            
            elif(char == '1' or char == '2' or char == '3' or char == '4' or char == '5' or char == '6' or char == '7' or char == '8'):
                piece = Pieces.EMPTY
                count = ord(char) - ord('0')
                
            elif(char == '/' or char == ' '):
                rank -= 1
                file = Files.A
                continue
            else:
                print("Wrong FEN")
                return False
            for i in range(0, count):
                sq64 = rank * 8 + file # calculating the sqaure64 using file and rank for example. D4 -> 27
                sq120 = Sq64ToSq120[sq64]
                if(piece != Pieces.EMPTY):
                    self.pieces[sq120] = piece
                file += 1
        
        self.side = Colors.WHITE if fen_parts[1] == 'w' else Colors.BLACK
        for castleCase in fen_parts[2]:
            if(castleCase == "K"):
                self.castlePerm |= Castling.WKCA
            elif(castleCase == "Q"):
                self.castlePerm |= Castling.WQCA
            elif(castleCase == "k"):
                self.castlePerm |= Castling.BKCA
            elif(castleCase == "q"):
                self.castlePerm |= Castling.BQCA
            else: 
                pass
        assert_condition(self.castlePerm >= 0 and self.castlePerm <= 15)
        
        if(fen_parts[3] != "-"):
            file = ord(fen_parts[3][0]) - ord('a')
            rank = ord(fen_parts[3][1]) - ord('1')
            
            assert_condition(file >= Files.A and file <= Files.H)
            assert_condition(rank >= Ranks.R1 and rank <= Ranks.R8)
            self.enPas = FR2SQ(file, rank)
        self.posKey.generate_key(self) #generating the hashkey
        self.update_list_material()
        return True

    def check_board(self):
        if(not DEBUG):
            return True
        
        t_pceNum = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        t_bigPce = [0,0]
        t_majPce = [0,0]
        t_minPce = [0,0]
        t_material = [0,0]
        
        t_pawns = [0, 0, 0]
        t_pawns[Colors.WHITE] = self.pawns[Colors.WHITE]
        t_pawns[Colors.BLACK] = self.pawns[Colors.BLACK]
        t_pawns[Colors.BOTH] = self.pawns[Colors.BOTH]
        
        
        # check piece lists
        for t_piece in range(Pieces.wP, Pieces.bK+1):
            for t_pce_num in range(0, self.pceNum[t_piece]): # lets say we have 3 white pawns, this loop will loop form 0 - 2
                sq120 = self.pList[t_piece][t_pce_num] # getting the sqaure of the pawn
                assert_condition(self.pieces[sq120] == t_piece, message="Mismatch between the pList and pieces (12x10 board)") # checking if on actual 12x10 board, that piece exists on that square or not
                
        # check piece count and other counters
        for sq64 in range(0, 64):
            sq120 = Sq64ToSq120[sq64]
            t_piece = self.pieces[sq120]
            if(t_piece != 0):
                t_pceNum[t_piece] += 1 #incrementing the no. of pieces, 
                colour = PieceCol[t_piece]
                
                if(PieceBig[t_piece]):
                    t_bigPce[colour] += 1
                if(PieceMin[t_piece]):
                    t_minPce[colour] += 1
                if(PieceMaj[t_piece]):
                    t_majPce[colour] += 1
                
                t_material[colour] += PieceVal[t_piece]
            
        for t_piece in range(Pieces.wP, Pieces.bK+1):
            assert_condition(t_pceNum[t_piece] == self.pceNum[t_piece], message="Piece Number Not Matched!") #checking if the piece number on the board is equal to the piece num we calculated
            
        # check pawn bitboards
        pcount = CountBits(t_pawns[Colors.WHITE])
        assert_condition(pcount == self.pceNum[Pieces.wP], message="Mismatch between WHITE Pawns Bitboard and No. of White Pawns")
        pcount = CountBits(t_pawns[Colors.BLACK])
        assert_condition(pcount == self.pceNum[Pieces.bP], message="Mismatch between BLACK Pawns Bitboard and No. of BLack Pawns")
        pcount = CountBits(t_pawns[Colors.BOTH])
        assert_condition(pcount == self.pceNum[Pieces.wP] + self.pceNum[Pieces.bP], message="Mismatch between BOTH Pawns Bitboard and No. of BOTH Pawns")
        
        #check bitboards square
        tp = t_pawns[Colors.WHITE]
        while(tp):
            sq64, tp = PopBit(tp)
            assert_condition(self.pieces[Sq64ToSq120[sq64]] == Pieces.wP, message="WHITE Pawn on bitboard and actual Board not Matched!!")
            
        tp = t_pawns[Colors.BLACK]
        while(tp):
            sq64, tp = PopBit(tp)
            assert_condition(self.pieces[Sq64ToSq120[sq64]] == Pieces.bP, message="BLACK Pawn on bitboard and actual Board not Matched!!")
            
        tp = t_pawns[Colors.BOTH]
        while(tp):
            sq64, tp = PopBit(tp)
            assert_condition((self.pieces[Sq64ToSq120[sq64]] == Pieces.wP) or (self.pieces[Sq64ToSq120[sq64]] == Pieces.bP), message="WHITE or BLACK Pawn on bitboard and actual Board not Matched!!")
            
        assert_condition(t_material[Colors.WHITE] == self.material[Colors.WHITE] and t_material[Colors.BLACK] == self.material[Colors.BLACK], message="Material Value Not Matched!!")
        
        assert_condition(t_minPce[Colors.WHITE] == self.minPce[Colors.WHITE] and t_minPce[Colors.BLACK] == self.minPce[Colors.BLACK], message="Number of Min Pieces not Matched!!")
        
        assert_condition(t_majPce[Colors.WHITE] == self.majPce[Colors.WHITE] and t_majPce[Colors.BLACK] == self.majPce[Colors.BLACK], message="Number of Maj Pieces not Matched!!")
        
        assert_condition(t_bigPce[Colors.WHITE] == self.bigPce[Colors.WHITE] and t_bigPce[Colors.BLACK] == self.bigPce[Colors.BLACK], message="Number of Big (Non-Pawn) Pieces not Matched!!")
        
        assert_condition(self.side == Colors.WHITE or self.side == Colors.BLACK, message="SIDE can either be WHITE or BLACK")
        assert_condition(self.enPas == Squares.NO_SQ or (RanksBrd[self.enPas] == Ranks.R6 and self.side == Colors.WHITE) or (RanksBrd[self.enPas] == Ranks.R3 and self.side == Colors.BLACK), message="Invalid EnPas Square") # enPas square is either on rank 3 or rank 6
        
        assert_condition(self.pieces[self.king_square[Colors.WHITE]] == Pieces.wK, message="WHITE King Square not Matched!!")
        assert_condition(self.pieces[self.king_square[Colors.BLACK]] == Pieces.bK, message="BLACK King Square not Matched!!")
        
        return True

    def clear_piece(self, sq):
        assert_condition(SqOnBoard(sq))
    
        pce = self.pieces[sq]
        assert_condition(PieceValid(pce))
        
        self.posKey.hash_piece(piece=pce, square=sq)
        
        col = PieceCol[pce] # getting the color of the piece
        self.pieces[sq] = Pieces.EMPTY # making that square empty
        self.material[col] -= PieceVal[pce] # subtracting its value
        
        if(PieceBig[pce]): # if its a non-pawn piece
            self.bigPce[col] -= 1
            if(PieceMaj[pce]): # if its a rook or queen (major pieces)
                self.majPce[col] -= 1 
            else: # if its a minor piece (knights , bishops)
                self.minPce[col] -= 1
        else: # if its a pawn
            self.pawns[col] = ClearBit(self.pawns[col], Sq120ToSq64[sq]) # bitboard, sq64
            self.pawns[Colors.BOTH] = ClearBit(self.pawns[Colors.BOTH], Sq120ToSq64[sq])


        # removing that particular piece from the pList[][]  
        t_pceIndex = -1
        for index in range(0, self.pceNum[pce]): # looping all the pieces , for example, lets say we want to clear a white pawn on e4, we loop all the whitePawns
            if(self.pList[pce][index] == sq): # we find the index of whitePawn on e4 sqaure particularly
                t_pceIndex = index
                break   
        
        assert_condition(t_pceIndex != -1) # if the t_pceIndex is still not changed, then we have a mismatch on our pieces and pList, we need to debug
        self.pceNum[pce] -= 1 # decrementing pceNum, because we cleared one piece
        # following line , does what is, it places the last piece 's square on the index of the piece we captured
        # ?why because, we decremented the pceNum, instead of shifting all the [piece][] & squares, we just move the last one.
        self.pList[pce][t_pceIndex] = self.pList[pce][self.pceNum[pce]]

    def add_piece(self, sq, pce):
        assert_condition(PieceValid(pce))
        assert_condition(SqOnBoard(sq))
        
        col = PieceCol[pce]
        self.posKey.hash_piece(piece=pce, square=sq)
        
        self.pieces[sq] = pce
        
        if(PieceBig[pce]):
            self.bigPce[col] += 1
            if(PieceMaj[pce]):
                self.majPce[col] += 1
            else:
                self.minPce[col] += 1
        else: 
            self.pawns[col] = SetBit(self.pawns[col], Sq120ToSq64[sq])
            self.pawns[Colors.BOTH] = SetBit(self.pawns[Colors.BOTH], Sq120ToSq64[sq])
            
        self.material[col] += PieceVal[pce] #updating the material value
        self.pList[pce][self.pceNum[pce]] = sq # setting the pce on pList
        self.pceNum[pce] += 1

    def move_piece(self, fromSq, toSq):
        assert_condition(SqOnBoard(fromSq))
        assert_condition(SqOnBoard(toSq))
        
        pce = self.pieces[fromSq]
        col = PieceCol[pce]
        
        t_PieceIndex = False
        
        self.posKey.hash_piece(piece=pce, square=fromSq)
        self.pieces[fromSq] = Pieces.EMPTY
        
        self.posKey.hash_piece(piece=pce, square=toSq)
        self.pieces[toSq] = pce
        
        if(not PieceBig[pce]): # if its a pawn
            self.pawns[col] = ClearBit(self.pawns[col], Sq120ToSq64[fromSq])
            self.pawns[Colors.BOTH] = ClearBit(self.pawns[Colors.BOTH], Sq120ToSq64[fromSq])
            self.pawns[col] = SetBit(self.pawns[col], Sq120ToSq64[toSq])
            self.pawns[Colors.BOTH] = SetBit(self.pawns[Colors.BOTH], Sq120ToSq64[toSq])
            
        for index in range(0, self.pceNum[pce]):
            if(self.pList[pce][index] == fromSq):
                self.pList[pce][index] = toSq
                t_PieceIndex = True
                break
        
        assert_condition(t_PieceIndex)
        
    def take_move(self):
        assert_condition(self.check_board())
        
        # resetting the counters
        self.hisPly -= 1
        self.ply -= 1
        
        move = self.history[self.hisPly].move # getting the move from the history
        fromSq = move.FROMSQ()
        toSq = move.TOSQ()
        
        assert_condition(SqOnBoard(fromSq))
        assert_condition(SqOnBoard(toSq))
        
        if(self.enPas != Squares.NO_SQ):
            self.posKey.hash_enPas(enPas=self.enPas)
        self.posKey.hash_castle(castlePerm=self.castlePerm) # hashing out the current castle Perm
        
        self.castlePerm = self.history[self.hisPly].castlePerm # retreiving back the previous castlePerm
        self.fiftyMove = self.history[self.hisPly].fiftyMove
        self.enPas = self.history[self.hisPly].enPas
        
        if(self.enPas != Squares.NO_SQ):
            self.posKey.hash_enPas(enPas=self.enPas)
        self.posKey.hash_castle(castlePerm=self.castlePerm) # hashing in the new castle permission
        
        self.side ^= 1 #changing back the side
        self.posKey.hash_side()
        
        if(move.move & MOVE.FLAG_EP): # if it was an enPas capture, then we add back the pieces
            if(self.side == Colors.WHITE):
                self.add_piece(toSq-10, Pieces.bP)
            else:
                self.add_piece(toSq+10, Pieces.wP)
                
        elif(move.move & MOVE.FLAG_CA): # if it was a castle move
            if(toSq == Squares.C1):
                self.move_piece(Squares.D1, Squares.A1) # moving back the rook
            elif(toSq == Squares.C8):
                self.move_piece(Squares.D8, Squares.A8) # moving back the rook
            elif(toSq == Squares.G1):
                self.move_piece(Squares.F1, Squares.H1) # moving back the rook
            elif(toSq == Squares.G8):
                self.move_piece(Squares.F8, Squares.H8) # moving back the rook
            else:
                assert_condition(False)
                
        # moving back the piece
        self.move_piece(toSq, fromSq)
        
        if(PieceKing[self.pieces[fromSq]]):
            self.king_square[self.side] = fromSq # moving back the king
            
        captured = move.CAPTURED()
        if(captured != Pieces.EMPTY):
            assert_condition(PieceValid(captured))
            self.add_piece(toSq, captured) # adding back the captured piece
            
        prPce = move.PROMOTED()
        if(prPce != Pieces.EMPTY): #  ! explanation is needed
            assert_condition(PieceValid(prPce) and not PiecePawn[prPce])
            self.clear_piece(fromSq)
            toAdd = Pieces.wP if PieceCol[prPce] == Colors.WHITE else Pieces.bP
            self.add_piece(fromSq, toAdd)
        
        assert_condition(self.check_board())

    # it returns false (meaning illegal move) when? when after making the move, the king of the side which made the move is in CHECK.
    def make_move(self, move: MOVE) -> bool:
        assert_condition(self.check_board())
        fromSq = move.FROMSQ()
        toSq = move.TOSQ()
        side = self.side
        
        assert_condition(SqOnBoard(fromSq))
        assert_condition(SqOnBoard(toSq))
        assert_condition(SideValid(side))
        assert_condition(PieceValid(self.pieces[fromSq]))
        
        # storing the move in history, before changing any posKey, we store the posKey in history
        self.history[self.hisPly].posKey = self.posKey # history array contains the objects of class UNDO()
        
        if(move.move & MOVE.FLAG_EP): # if its an enpassant capture
            if(side == Colors.WHITE):
                self.clear_piece(toSq-10) # capturing the black pawn
            else:
                self.clear_piece(toSq+10) # capturing the white pawn
        elif(move.move & MOVE.FLAG_CA): # if its an castle MOVE
            if(toSq == Squares.C1):
                self.move_piece(Squares.A1, Squares.D1)
            elif(toSq == Squares.C8):
                self.move_piece(Squares.A8, Squares.D8)
            elif(toSq == Squares.G1): # white king side castling
                self.move_piece(Squares.H1, Squares.F1) # moving the rook from h1 -> f1
            elif(toSq == Squares.G8):
                self.move_piece(Squares.H8, Squares.F8)
            else:
                assert_condition(False)
                
        if(self.enPas != Squares.NO_SQ):
            self.posKey.hash_enPas(enPas=self.enPas)
            
        self.posKey.hash_castle(castlePerm=self.castlePerm) # hashing out the castle permission
        
        self.history[self.hisPly].move = move
        self.history[self.hisPly].fiftyMove = self.fiftyMove
        self.history[self.hisPly].enPas = self.enPas
        self.history[self.hisPly].castlePerm = self.castlePerm
        
        self.castlePerm &= CastlePerm[fromSq] # if king or rook has moved
        self.castlePerm &= CastlePerm[toSq] # if rook or king has moved
        self.enPas = Squares.NO_SQ
        
        self.posKey.hash_castle(castlePerm=self.castlePerm) # hashing in the new castle permission
        
        captured = move.CAPTURED()
        self.fiftyMove += 1
        
        if(captured != Pieces.EMPTY):
            assert_condition(PieceValid(captured))
            self.clear_piece(toSq) # first we capture on the toSq, then we move
            self.fiftyMove = 0 # if a capture is made, then fifty move is set to 0
        
        self.hisPly += 1
        self.ply += 1
        
        # setting up the enPas sqaure
        if(PiecePawn[self.pieces[fromSq]]): # if the piece on fromSq was a pawn
            self.fiftyMove = 0 # if its a pawn move, reset the counter
            if(move.move & MOVE.FLAG_PS): # if it was a pawn start move
                if(side == Colors.WHITE):
                    self.enPas = fromSq + 10
                    assert_condition(RanksBrd[self.enPas] == Ranks.R3)
                else:
                    self.enPas = fromSq - 10
                    assert_condition(RanksBrd[self.enPas] == Ranks.R6)
                self.posKey.hash_enPas(enPas=self.enPas) # hashing in the new enPas
        
        # finally moving the piece on the board
        self.move_piece(fromSq, toSq)
        
        # checking for promotions
        prPce = move.PROMOTED()
        if(prPce != Pieces.EMPTY):
            assert_condition(PieceValid(prPce) and not PiecePawn[prPce])
            
            # ! explanation needed
            self.clear_piece(toSq) # clearing the toSq
            self.add_piece(toSq, prPce) # adding the promoted piece on the toSq
            
        # updating the king_squareuare
        if(PieceKing[self.pieces[toSq]]):
            self.king_square[self.side] = toSq
        
        self.side ^= 1 # changing the side
        self.posKey.hash_side()
        
        assert_condition(self.check_board())
        
        if(is_sqaure_attacked(self.king_square[side], self.side, self)): # side is the side which made the move, self.side now is now the opposite side, so we check if after making the move, the opposite side is attacking the king_square, means king is in check, then its an illegal move
            self.take_move()  # take back the move
            return False
        
        return True

    def is_repetition(self) -> bool :
        for index in range(self.hisPly - self.fiftyMove, self.hisPly-1): # checking from only when last time fiftyMove was set to 0 because once fifty move is set to 0 there won't be no repetetions(captures and pawn moves cant repeat)
            if(self.posKey.key == self.history[index].posKey.key):
                assert_condition(index >=0 and index <= MAXGAMEMOVES)
                return True
            
        return False
    
    def evaluate_position(self) -> int:
        pce = 0
        score = self.material[Colors.WHITE] - self.material[Colors.BLACK]
        
        pce=Pieces.wP
        for pceNum in range(0, self.pceNum[pce]): # traversing all the white pawns
            sq = self.pList[pce][pceNum] # getting the 120 based square on which the piece is
            assert_condition(SqOnBoard(sq))
            score += PawnTable[Sq120ToSq64[sq]]
        
        pce=Pieces.bP
        for pceNum in range(0, self.pceNum[pce]): # traversing all the black pawns
            sq = self.pList[pce][pceNum] # getting the 120 based square on which the piece is
            assert_condition(SqOnBoard(sq))
            score -= PawnTable[Mirror64[Sq120ToSq64[sq]]] # mirroring the square for black
            
        pce=Pieces.wN
        for pceNum in range(0, self.pceNum[pce]): # traversing all the white knights
            sq = self.pList[pce][pceNum] # getting the 120 based square on which the piece is
            assert_condition(SqOnBoard(sq))
            score += KnightTable[Sq120ToSq64[sq]]
        
        pce=Pieces.bN
        for pceNum in range(0, self.pceNum[pce]): # traversing all the black knights
            sq = self.pList[pce][pceNum] # getting the 120 based square on which the piece is
            assert_condition(SqOnBoard(sq))
            score -= KnightTable[Mirror64[Sq120ToSq64[sq]]] # mirroring the square for black
            
        pce=Pieces.wB
        for pceNum in range(0, self.pceNum[pce]): # traversing all the white bishops
            sq = self.pList[pce][pceNum] # getting the 120 based square on which the piece is
            assert_condition(SqOnBoard(sq))
            score += BishopTable[Sq120ToSq64[sq]]
        
        pce=Pieces.bB
        for pceNum in range(0, self.pceNum[pce]): # traversing all the black bishops
            sq = self.pList[pce][pceNum] # getting the 120 based square on which the piece is
            assert_condition(SqOnBoard(sq))
            score -= BishopTable[Mirror64[Sq120ToSq64[sq]]] # mirroring the square for black
            
        pce=Pieces.wR
        for pceNum in range(0, self.pceNum[pce]): # traversing all the white rooks
            sq = self.pList[pce][pceNum] # getting the 120 based square on which the piece is
            assert_condition(SqOnBoard(sq))
            score += RookTable[Sq120ToSq64[sq]]
        
        pce=Pieces.bR
        for pceNum in range(0, self.pceNum[pce]): # traversing all the black rooks
            sq = self.pList[pce][pceNum] # getting the 120 based square on which the piece is
            assert_condition(SqOnBoard(sq))
            score -= RookTable[Mirror64[Sq120ToSq64[sq]]] # mirroring the square for black
            
        if(self.side == Colors.WHITE):
            return score
        else:
            return -score # negating the score for black (because we are calculating score based on white, lets say black's score is better than our score value will be -ve because score = whiteMaterial - blackMaterial and later on we are subtracting for black and adding for white)
        
    