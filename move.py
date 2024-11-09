from globals import FilesBrd, RanksBrd
from globals import *
from debug import assert_condition
from validate import SqOnBoard, PieceValid, PieceValidEmpty
from constants import SQUARES, PIECE, RANK, CASTLING
from attack import is_sqaure_attacked

def SQOFFBOARD(sq):
    return FilesBrd[sq] == SQUARES.OFFBOARD.value

class MOVE:
    # move flags, to retrieve information from the move
    FLAG_EP = 0x40000 # to check if the capture was EnPassant or not
    FLAG_PS = 0x80000 # to check if it was a pawn move
    FLAG_CA = 0x1000000 # to check if it was a castle move
    FLAG_CAP = 0x7C000 # to check if there occured any capture at all
    FLAG_PROM = 0xF00000 # to check if there occured any promotion of pawn
    def __init__(self, fromSq=0, toSq=0, captured=0, prom=0, flag=0):
        self.move = (fromSq | (toSq << 7) | (captured << 14) | (prom << 20) | flag)
        # move represents the following information in 25 bits
        # FROM (square)(21 - 98)  - 7 bits
        # TO (square) - 7 bits
        # Captured Piece (0 - 12) - 4 bits
        # EnPas Capture? (0 - 1) - 1 bit
        # Pawn Start ? (0 - 1) - 1 bit
        # Promoted Piece (0 - 12) - 4 bits
        # castle move? (0 - 1) - 1 bit
        self.score = 0
        
    def FROMSQ(self):
        return self.move & 0x7F #extracting the last 7 bits from the move number
    
    def TOSQ(self):
        return (self.move >> 7) & 0x7F # first right shift the bits to 7 and then extract the last 7 bits which represents now TO Square
    
    def CAPTURED(self):
        return (self.move >> 14) & 0xF
    
    def PROMOTED(self):
        return (self.move >> 20) & 0xF
    
    def alpha_move(self):
        ff = FilesBrd[self.FROMSQ()] # file from 
        rf = RanksBrd[self.FROMSQ()] # rank from 
        ft = FilesBrd[self.TOSQ()] # file TO
        rt = RanksBrd[self.TOSQ()] # rank TO
        
        promoted = self.PROMOTED() # promoted piece value
        
        if(promoted):
            pchar = 'q'
            if(PieceKnight[promoted]): # if promoted piece was a knight
                pchar = 'n'
            elif(PieceRookQueen[promoted] and not PieceBishopQueen[promoted]):
                pchar = 'r'
            elif(not PieceRookQueen[promoted] and PieceBishopQueen[promoted]):
                pchar = 'b'
            MvStr = "{}{}{}{}{}".format(chr(ord('a') + ff), chr(ord('1') + rf), chr(ord('a') + ft), chr(ord('1') + rt), pchar)
        else:
            MvStr = "{}{}{}{}".format(chr(ord('a') + ff), chr(ord('1') + rf), chr(ord('a') + ft), chr(ord('1') + rt))
            
        return MvStr
    
    def move_exists(self, board) -> bool:
        mlist = MOVELIST()
        mlist.generate_all_moves(board)
        
        for MoveNum in range(0, mlist.count):
            if(not board.make_move(mlist.moves[MoveNum].move) ):
                continue
            
            board.take_move()
            if(mlist.moves[MoveNum].move.move == self.move):
                return True
        
        return False
    
class MOVELIST:
    def __init__(self):
        self.moves = [MOVE() for _ in range(256)]
        self.count = 0
        
    def add_quite_move(self, board, move: MOVE):
        assert_condition(SqOnBoard(move.FROMSQ()))
        assert_condition(SqOnBoard(move.TOSQ()))
        self.moves[self.count].move = move
        self.moves[self.count].score = 0
        
        if(board.searchKillers[0][board.ply] == move):
            self.moves[self.count].score = 900000
        elif (board.searchKillers[1][board.ply] == move):
            self.moves[self.count].score = 800000
        else:
            self.moves[self.count].score = board.searchHistory[board.pieces[move.FROMSQ()]][move.TOSQ()]
        self.count += 1
        
    def add_capture_move(self, board, move: MOVE):
        assert_condition(SqOnBoard(move.FROMSQ()))
        assert_condition(SqOnBoard(move.TOSQ()))
        assert_condition(PieceValid(move.CAPTURED()))
        self.moves[self.count].move = move
        self.moves[self.count].score = MvvLvaScores[move.CAPTURED()][board.pieces[move.FROMSQ()]] + 1000000 # victim , attacker
        self.count += 1
        
    def add_enpas_move(self, board, move: MOVE):
        assert_condition(SqOnBoard(move.FROMSQ()))
        assert_condition(SqOnBoard(move.TOSQ()))
        self.moves[self.count].move = move
        self.moves[self.count].score = 105 + 1000000 # pawn takes pawn
        self.count += 1
        
    def add_white_pawn_cap_move(self, board, fromSq, toSq, cap):
        assert_condition(SqOnBoard(fromSq))
        assert_condition(SqOnBoard(toSq))
        assert_condition(PieceValidEmpty(cap))
        
        if(RanksBrd[fromSq] == RANK.R7.value): # if a white pawn captures something from rank 7, then it is promotion move
            self.add_capture_move(board, MOVE(fromSq, toSq,cap,PIECE.wQ.value, 0)) # promoted to white Queen
            self.add_capture_move(board, MOVE(fromSq, toSq,cap,PIECE.wR.value, 0)) # promoted to white Rook
            self.add_capture_move(board, MOVE(fromSq, toSq,cap,PIECE.wB.value, 0)) # promoted to white Bishop
            self.add_capture_move(board, MOVE(fromSq, toSq,cap,PIECE.wN.value, 0)) # promoted to white Knight
        else: # if it is not an promotion move
            self.add_capture_move(board, MOVE(fromSq, toSq, cap, PIECE.EMPTY.value, 0))
            
    def add_white_pawn_move(self, board, fromSq, toSq): # same as above, the difference is it doesn't capture any piece
        assert_condition(SqOnBoard(fromSq))
        assert_condition(SqOnBoard(toSq))
        if(RanksBrd[fromSq] == RANK.R7.value): # if a white pawn captures something from rank 7, then it is promotion move
            self.add_quite_move(board, MOVE(fromSq, toSq,PIECE.EMPTY.value,PIECE.wQ.value, 0)) # promoted to white Queen
            self.add_quite_move(board, MOVE(fromSq, toSq,PIECE.EMPTY.value,PIECE.wR.value, 0)) # promoted to white Rook
            self.add_quite_move(board, MOVE(fromSq, toSq,PIECE.EMPTY.value,PIECE.wB.value, 0)) # promoted to white Bishop
            self.add_quite_move(board, MOVE(fromSq, toSq,PIECE.EMPTY.value,PIECE.wN.value, 0)) # promoted to white Knight
        else: # if it is not an promotion move
            self.add_quite_move(board, MOVE(fromSq, toSq, PIECE.EMPTY.value, PIECE.EMPTY.value, 0))
            
    def add_black_pawn_cap_move(self, board, fromSq, toSq, cap):
        assert_condition(SqOnBoard(fromSq))
        assert_condition(SqOnBoard(toSq))
        assert_condition(PieceValidEmpty(cap))
        if(RanksBrd[fromSq] == RANK.R2.value): # if a black pawn captures something from rank 2, then it is promotion move
            self.add_capture_move(board, MOVE(fromSq, toSq,cap,PIECE.bQ.value, 0)) # promoted to black Queen
            self.add_capture_move(board, MOVE(fromSq, toSq,cap,PIECE.bR.value, 0)) # promoted to black Rook
            self.add_capture_move(board, MOVE(fromSq, toSq,cap,PIECE.bB.value, 0)) # promoted to black Bishop
            self.add_capture_move(board, MOVE(fromSq, toSq,cap,PIECE.bN.value, 0)) # promoted to black Knight
        else: # if it is not an promotion move
            self.add_capture_move(board, MOVE(fromSq, toSq, cap, PIECE.EMPTY.value, 0))
            
    def add_black_pawn_move(self, board, fromSq, toSq):
        assert_condition(SqOnBoard(fromSq))
        assert_condition(SqOnBoard(toSq))
        if(RanksBrd[fromSq] == RANK.R2.value): # if a Black pawn captures something from rank 2, then it is promotion move
            self.add_quite_move(board, MOVE(fromSq, toSq,PIECE.EMPTY.value,PIECE.bQ.value, 0)) # promoted to Black Queen
            self.add_quite_move(board, MOVE(fromSq, toSq,PIECE.EMPTY.value,PIECE.bR.value, 0)) # promoted to Black Rook
            self.add_quite_move(board, MOVE(fromSq, toSq,PIECE.EMPTY.value,PIECE.bB.value, 0)) # promoted to Black Bishop
            self.add_quite_move(board, MOVE(fromSq, toSq,PIECE.EMPTY.value,PIECE.bN.value, 0)) # promoted to Black Knight
        else: # if it is not an promotion move
            self.add_quite_move(board, MOVE(fromSq, toSq, PIECE.EMPTY.value, PIECE.EMPTY.value, 0))
        
    def generate_all_moves(self, board):
        assert_condition(board.check_board())
    
        # generating white pawn moves
        self.count = 0
        pce = PIECE.EMPTY.value
        side = board.side
        sq = 0
        t_sq = 0
        
        if(side == COLORS.WHITE.value):
            # looping to total number of white pawns on the board
            for pceNum in range(0, board.pceNum[PIECE.wP.value]):
                sq = board.pList[PIECE.wP.value][pceNum] # to get the square on which there is a white Pawn
                assert_condition(SqOnBoard(sq))
                
                # if it is a no capture move
                if(board.pieces[sq + 10] == PIECE.EMPTY.value):
                    self.add_white_pawn_move(board, sq, sq+10) # board, fromSq, ToSq
                    #
                    if(RanksBrd[sq] == RANK.R2.value and board.pieces[sq + 20] == PIECE.EMPTY.value):
                        self.add_quite_move(board, MOVE(sq, sq+20, PIECE.EMPTY.value, PIECE.EMPTY.value, MOVE.FLAG_PS)) # added a quite move, because there was no capture, also setted the Pawn Start Flag
                        
                # if it is a capture move            
                if(not SQOFFBOARD(sq + 9) and PieceCol[board.pieces[sq + 9]] == COLORS.BLACK.value): # if the capturing piece is black
                    self.add_white_pawn_cap_move(board, sq, sq+9, board.pieces[sq+9]) # board, fromSq, ToSq, CapturedPiece
                    
                if(not SQOFFBOARD(sq + 11) and PieceCol[board.pieces[sq + 11]] == COLORS.BLACK.value): # if the capturing piece is black
                    self.add_white_pawn_cap_move(board, sq, sq+11, board.pieces[sq+11]) # board, fromSq, ToSq, CapturedPiece
                if(board.enPas != SQUARES.NO_SQ.value):
                    if(sq + 9 == board.enPas):
                        self.add_enpas_move(board, MOVE(sq, sq+9, PIECE.EMPTY.value, PIECE.EMPTY.value, MOVE.FLAG_EP))
                    if(sq + 11 == board.enPas):
                        self.add_enpas_move(board, MOVE(sq, sq+11, PIECE.EMPTY.value, PIECE.EMPTY.value, MOVE.FLAG_EP))
                    
            # castling for white
            # king side castling
            if(board.castlePerm & CASTLING.WKCA.value): #if white can castle king side
                if(board.pieces[SQUARES.F1.value] == PIECE.EMPTY.value and board.pieces[SQUARES.G1.value] == PIECE.EMPTY.value): # if between the king and rook squares are empty
                    if(not is_sqaure_attacked(SQUARES.E1.value, COLORS.BLACK.value, board) and not is_sqaure_attacked(SQUARES.F1.value, COLORS.BLACK.value, board)): # if the square F1, E1 are not attacked, only then king can castle, beacause, king cannot castle in between check
                        
                        # adding the castle move white king side castle
                        self.add_quite_move(board, MOVE(SQUARES.E1.value, SQUARES.G1.value, PIECE.EMPTY.value, PIECE.EMPTY.value, MOVE.FLAG_CA))
                        
            if(board.castlePerm & CASTLING.WQCA.value):
                if(board.pieces[SQUARES.D1.value] == PIECE.EMPTY.value and board.pieces[SQUARES.C1.value] == PIECE.EMPTY.value and board.pieces[SQUARES.B1.value] == PIECE.EMPTY.value): # if between the king and rook squares are empty
                    if(not is_sqaure_attacked(SQUARES.E1.value, COLORS.BLACK.value, board) and not is_sqaure_attacked(SQUARES.D1.value, COLORS.BLACK.value, board)): # if the square D1, E1 are not attacked, only then king can castle, beacause, king cannot castle in between check
                        
                        # adding the castle move white queen side castle
                        self.add_quite_move(board, MOVE(SQUARES.E1.value, SQUARES.C1.value, PIECE.EMPTY.value, PIECE.EMPTY.value, MOVE.FLAG_CA))
        else: 
            # looping to total number of black pawns on the board
            for pceNum in range(0, board.pceNum[PIECE.bP.value]):
                sq = board.pList[PIECE.bP.value][pceNum] # to get the square on which there is a black Pawn
                assert_condition(SqOnBoard(sq))
                
                # if it is a no capture move
                if(board.pieces[sq - 10] == PIECE.EMPTY.value):
                    self.add_black_pawn_move(board, sq, sq-10) # board, fromSq, ToSq
                    #
                    if(RanksBrd[sq] == RANK.R7.value and board.pieces[sq - 20] == PIECE.EMPTY.value):
                        self.add_quite_move(board, MOVE(sq, sq-20, PIECE.EMPTY.value, PIECE.EMPTY.value, MOVE.FLAG_PS)) # added a quite move, because there was no capture, also setted the Pawn Start Flag
                        
                # if it is a capture move            
                if(not SQOFFBOARD(sq - 9) and PieceCol[board.pieces[sq - 9]] == COLORS.WHITE.value): # if the capturing piece is WHITE
                    self.add_black_pawn_cap_move(board, sq, sq-9, board.pieces[sq-9]) # board, fromSq, ToSq, CapturedPiece
                    
                if(not SQOFFBOARD(sq - 11) and PieceCol[board.pieces[sq - 11]] == COLORS.WHITE.value): # if the capturing piece is WHITE
                    self.add_black_pawn_cap_move(board, sq, sq-11, board.pieces[sq-11]) # board, fromSq, ToSq, CapturedPiece
                if(board.enPas != SQUARES.NO_SQ.value):
                    if(sq - 9 == board.enPas):
                        self.add_enpas_move(board, MOVE(sq, sq-9, PIECE.EMPTY.value, PIECE.EMPTY.value, MOVE.FLAG_EP))
                    if(sq - 11 == board.enPas):
                        self.add_enpas_move(board, MOVE(sq, sq-11, PIECE.EMPTY.value, PIECE.EMPTY.value, MOVE.FLAG_EP))
                    
            # castling for black
            # king side castling
            if(board.castlePerm & CASTLING.BKCA.value):
                if(board.pieces[SQUARES.F8.value] == PIECE.EMPTY.value and board.pieces[SQUARES.G8.value] == PIECE.EMPTY.value): # if between the king and rook squares are empty
                    if(not is_sqaure_attacked(SQUARES.E8.value, COLORS.WHITE.value, board) and not is_sqaure_attacked(SQUARES.F8.value, COLORS.WHITE.value, board)): # if the square F8, E8 are not attacked, only then king can castle, beacause, king cannot castle in between check
                        
                        # adding the castle move black king side castle
                        self.add_quite_move(board, MOVE(SQUARES.E8.value, SQUARES.G8.value, PIECE.EMPTY.value, PIECE.EMPTY.value, MOVE.FLAG_CA))
                        
            if(board.castlePerm & CASTLING.BQCA.value):
                if(board.pieces[SQUARES.D8.value] == PIECE.EMPTY.value and board.pieces[SQUARES.C8.value] == PIECE.EMPTY.value and board.pieces[SQUARES.B8.value] == PIECE.EMPTY.value): # if between the king and rook squares are empty
                    if(not is_sqaure_attacked(SQUARES.E8.value, COLORS.WHITE.value, board) and not is_sqaure_attacked(SQUARES.D8.value, COLORS.WHITE.value, board)): # if the square D8, E8 are not attacked, only then king can castle, beacause, king cannot castle in between check
                        
                        # adding the castle move black queen side castle
                        self.add_quite_move(board, MOVE(SQUARES.E8.value, SQUARES.C8.value, PIECE.EMPTY.value, PIECE.EMPTY.value, MOVE.FLAG_CA))

        # Move generation for sliding pieces (Bishops, Rooks, Queen)
        pceIndex = LoopSlideIndex[side] # WHITE - 0, BLACK - 4
        pce = LoopSlidePce[pceIndex] # for white First piece is White Bishop
        
        while(pce != 0):
            assert_condition(PieceValid(pce))
            pce = LoopSlidePce[pceIndex]
            for pceNum in range(0, board.pceNum[pce]):
                sq = board.pList[pce][pceNum] # accesing the square on which that particular piece is
                assert_condition(SqOnBoard(sq))
                
                #generating the moves
                for index in range(NumDir[pce]): # looping till no of directions for each piece
                    dir = PceDir[pce][index]
                    t_sq = sq + dir
                    
                    while(not SQOFFBOARD(t_sq)):   # for sliding pieces we need to iterate in that direction till we are offboard 
                        # capture move, BLACK(1) ^ 1 == WHITE(0)
                        if(board.pieces[t_sq] != PIECE.EMPTY.value):
                            if(PieceCol[board.pieces[t_sq]] == side ^ 1): # opposite color
                                
                                # addding a capture move
                                self.add_capture_move(board, MOVE(sq, t_sq, board.pieces[t_sq], PIECE.EMPTY.value, 0))
                                
                            break #if same color piece is found then break, we can't move further
                        
                        # Normal Move
                        self.add_quite_move(board, MOVE(sq, t_sq, PIECE.EMPTY.value, PIECE.EMPTY.value, 0))
                        t_sq += dir
            
            pceIndex += 1
        
        
        # Move generation for non sliding pieces (Knights, King)
        pceIndex = LoopNonSlideIndex[side] # WHITE - 0, BLACK - 4
        pce = LoopNonSlidePce[pceIndex] # for white First piece is White Knight
        
        while(pce != 0):
            assert_condition(PieceValid(pce))
            pce = LoopNonSlidePce[pceIndex]
            
            for pceNum in range(0, board.pceNum[pce]):
                sq = board.pList[pce][pceNum] # accesing the square on which that particular piece is
                assert_condition(SqOnBoard(sq))
                
                #generating the moves
                for index in range(NumDir[pce]): # looping till no of directions for each piece
                    dir = PceDir[pce][index]
                    t_sq = sq + dir
                    if(SQOFFBOARD(t_sq)):
                        continue
                    
                    # capture move, BLACK(1) ^ 1 == WHITE(0)
                    if(board.pieces[t_sq] != PIECE.EMPTY.value):
                        if(PieceCol[board.pieces[t_sq]] == side ^ 1): # opposite color
                            # addding a capture move
                            self.add_capture_move(board, MOVE(sq, t_sq, board.pieces[t_sq], PIECE.EMPTY.value, 0))
                        continue #if same color then skip
                    
                    # Normal Move
                    self.add_quite_move(board, MOVE(sq, t_sq, PIECE.EMPTY.value, PIECE.EMPTY.value, 0))
            
            pceIndex += 1
            
    def generate_capture_moves(self, board):
        assert_condition(board.check_board())
        
        # generating white pawn moves
        self.count = 0
        pce = PIECE.EMPTY.value
        side = board.side
        sq = 0
        t_sq = 0
        
        if(side == COLORS.WHITE.value):
            # looping to total number of white pawns on the board
            for pceNum in range(0, board.pceNum[PIECE.wP.value]):
                sq = board.pList[PIECE.wP.value][pceNum] # to get the square on which there is a white Pawn
                assert_condition(SqOnBoard(sq))
                                    
                # if it is a capture move            
                if(not SQOFFBOARD(sq + 9) and PieceCol[board.pieces[sq + 9]] == COLORS.BLACK.value): # if the capturing piece is black
                    self.add_white_pawn_cap_move(board, sq, sq+9, board.pieces[sq+9]) # board, fromSq, ToSq, CapturedPiece, list
                    
                if(not SQOFFBOARD(sq + 11) and PieceCol[board.pieces[sq + 11]] == COLORS.BLACK.value): # if the capturing piece is black
                    self.add_white_pawn_cap_move(board, sq, sq+11, board.pieces[sq+11]) # board, fromSq, ToSq, CapturedPiece, list
                if(board.enPas != SQUARES.NO_SQ.value):
                    if(sq + 9 == board.enPas):
                        self.add_enpas_move(board, MOVE(sq, sq+9, PIECE.EMPTY.value, PIECE.EMPTY.value, MOVE.FLAG_EP))
                    if(sq + 11 == board.enPas):
                        self.add_enpas_move(board, MOVE(sq, sq+11, PIECE.EMPTY.value, PIECE.EMPTY.value, MOVE.FLAG_EP))
                    

        else: 
            # looping to total number of black pawns on the board
            for pceNum in range(0, board.pceNum[PIECE.bP.value]):
                sq = board.pList[PIECE.bP.value][pceNum] # to get the square on which there is a black Pawn
                assert_condition(SqOnBoard(sq))
                        
                # if it is a capture move            
                if(not SQOFFBOARD(sq - 9) and PieceCol[board.pieces[sq - 9]] == COLORS.WHITE.value): # if the capturing piece is WHITE
                    self.add_black_pawn_cap_move(board, sq, sq-9, board.pieces[sq-9]) # board, fromSq, ToSq, CapturedPiece, list
                    
                if(not SQOFFBOARD(sq - 11) and PieceCol[board.pieces[sq - 11]] == COLORS.WHITE.value): # if the capturing piece is WHITE
                    self.add_black_pawn_cap_move(board, sq, sq-11, board.pieces[sq-11]) # board, fromSq, ToSq, CapturedPiece, list
                if(board.enPas != SQUARES.NO_SQ.value):
                    if(sq - 9 == board.enPas):
                        self.add_enpas_move(board, MOVE(sq, sq-9, PIECE.EMPTY.value, PIECE.EMPTY.value, MOVE.FLAG_EP))
                    if(sq - 11 == board.enPas):
                        self.add_enpas_move(board, MOVE(sq, sq-11, PIECE.EMPTY.value, PIECE.EMPTY.value, MOVE.FLAG_EP))
                    
        # Move generation for sliding pieces (Bishops, Rooks, Queen)
        pceIndex = LoopSlideIndex[side] # WHITE - 0, BLACK - 4
        pce = LoopSlidePce[pceIndex] # for white First piece is White Bishop
        
        while(pce != 0):
            assert_condition(PieceValid(pce))
            pce = LoopSlidePce[pceIndex]
            for pceNum in range(0, board.pceNum[pce]):
                sq = board.pList[pce][pceNum] # accesing the square on which that particular piece is
                assert_condition(SqOnBoard(sq))
                
                #generating the moves
                for index in range(NumDir[pce]): # looping till no of directions for each piece
                    dir = PceDir[pce][index]
                    t_sq = sq + dir
                    
                    while(not SQOFFBOARD(t_sq)):   # for sliding pieces we need to iterate in that direction till we are offboard 
                        # capture move, BLACK(1) ^ 1 == WHITE(0)
                        if(board.pieces[t_sq] != PIECE.EMPTY.value):
                            if(PieceCol[board.pieces[t_sq]] == side ^ 1): # opposite color
                                
                                # addding a capture move
                                self.add_capture_move(board, MOVE(sq, t_sq, board.pieces[t_sq], PIECE.EMPTY.value, 0))
                                
                            break #if same color piece is found then break, we can't move further
                        
                        # Normal Move

                        t_sq += dir
            
            pceIndex += 1
        
        
        # Move generation for non sliding pieces (Knights, King)
        pceIndex = LoopNonSlideIndex[side] # WHITE - 0, BLACK - 4
        pce = LoopNonSlidePce[pceIndex] # for white First piece is White Knight
        
        while(pce != 0):
            assert_condition(PieceValid(pce))
            pce = LoopNonSlidePce[pceIndex]
            
            for pceNum in range(0, board.pceNum[pce]):
                sq = board.pList[pce][pceNum] # accesing the square on which that particular piece is
                assert_condition(SqOnBoard(sq))
                
                #generating the moves
                for index in range(NumDir[pce]): # looping till no of directions for each piece
                    dir = PceDir[pce][index]
                    t_sq = sq + dir
                    if(SQOFFBOARD(t_sq)):
                        continue
                    
                    # capture move, BLACK(1) ^ 1 == WHITE(0)
                    if(board.pieces[t_sq] != PIECE.EMPTY.value):
                        if(PieceCol[board.pieces[t_sq]] == side ^ 1): # opposite color
                            # addding a capture move
                            self.add_capture_move(board, MOVE(sq, t_sq, board.pieces[t_sq], PIECE.EMPTY.value, 0))
                        continue #if same color then skip
                    
                    # Normal Move
            
            pceIndex += 1
     