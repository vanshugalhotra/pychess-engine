from globals import *
from debug import _assert_condition
from validate import SqOnBoard, PieceValid, PieceValidEmpty
from constants import Pieces, Ranks, Castling, Squares
from attack import is_sqaure_attacked
from helper import FR2SQ

def SQOFFBOARD(sq):
    return FilesBrd[sq] == Squares.OFFBOARD

class MOVE:
    """
    Represents a chess move with encoded properties like source square, destination square, captured piece, promotion,
    and various flags for special moves.

    Class Variables:
        NOMOVE (MOVE): A static variable representing a non-existent or invalid move.
        FLAG_EP (int): Flag for en passant captures.
        FLAG_PS (int): Flag for pawn start moves.
        FLAG_CA (int): Flag for castling moves.
        FLAG_CAP (int): Flag for capture moves.
        FLAG_PROM (int): Flag for pawn promotion moves.
        
    Attributes:
        move (int): Encoded move information in 25 bits (source, destination, captured piece, promotion, flags).
        score (int): move score for evaluation purposes.

    Methods:
        FROMSQ(): Extracts and returns the source square of the move.
        TOSQ(): Extracts and returns the destination square of the move.
        CAPTURED(): Extracts and returns the captured piece code, if any.
        PROMOTED(): Extracts and returns the promotion piece code, if any.
        alpha_move() -> str: Converts the move to an algebraic notation string.
        move_exists(board) -> bool: Checks if the move exists on a given board by generating possible moves.
        parse_move(alpha_move: str, board) -> MOVE: Parses a move in algebraic notation to retrieve a matching MOVE instance.
    """
    NOMOVE = None
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
        
    def __str__(self):
        return self.alpha_move()
        
    def FROMSQ(self) -> int:
        """
        Extracts and returns the source square of the move.

        Returns:
            int: The 7-bit integer representing the source square of the move.
        """
        return self.move & 0x7F #extracting the last 7 bits from the move number
    
    def TOSQ(self) -> int:
        """
        Extracts and returns the destination square of the move.

        Returns:
            int: The 7-bit integer representing the destination square of the move.
        """
        return (self.move >> 7) & 0x7F # first right shift the bits to 7 and then extract the last 7 bits which represents now TO Square
    
    def CAPTURED(self) -> int:
        """
        Extracts and returns the captured piece type (if any) from the move.

        Returns:
            int: A 4-bit integer indicating the type of captured piece, or 0 if none.
        """    
        return (self.move >> 14) & 0xF
    
    def PROMOTED(self) -> int:
        """
        Extracts and returns the promoted piece type (if any) from the move

        Returns:
            int: A 4-bit integer representing the type of promoted piece, or 0 if no promotion occurred.
        """
        return (self.move >> 20) & 0xF
    
    def alpha_move(self) -> str:
        """
        Converts a move into its algebraic notation.

        This method constructs a string representing the move in algebraic format,

        Returns:
            str: A string representing the move in standard algebraic notation.
        """
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
        """
        Checks if a move exists in the list of all generated moves for the given board.

        This method generates all possible moves for the current board state and checks if
        the move represented by this instance exists in that list.

        Args:
            board(Board): The current board state on which to check if the move exists.

        Returns:
            bool: True if the move exists in the list of possible moves, False otherwise.
        """
        mlist = MOVELIST()
        mlist.generate_all_moves(board)
        
        for MoveNum in range(0, mlist.count):
            if(not board.make_move(mlist.moves[MoveNum]) ):
                continue
            
            board.take_move()
            if(mlist.moves[MoveNum].move == self.move):
                return True
        
        return False
    
    @staticmethod
    def parse_move(alpha_move: str, board): 
        """
        Parses a move from user input in algebraic notation (e.g., 'a2a3') and returns the corresponding MOVE object.
        
        Parameters:
            alpha_move (str): The move in algebraic notation.
            board (Board): The current board state.
        
        Returns:
            MOVE: The corresponding move object, or MOVE.NOMOVE if the move is invalid or not found.
        """
        _assert_condition(board._check_board())
        
        if(alpha_move[1] > '8' or alpha_move[1] < '1'):
            return MOVE.NOMOVE
        if(alpha_move[3] > '8' or alpha_move[3] < '1'):
            return MOVE.NOMOVE
        if(alpha_move[0] > 'h' or alpha_move[0] < 'a'):
            return MOVE.NOMOVE
        if(alpha_move[2] > 'h' or alpha_move[2] < 'a'):
            return MOVE.NOMOVE
        
        fromSq = FR2SQ(ord(alpha_move[0]) - ord('a'), ord(alpha_move[1]) - ord('1'))
        toSq = FR2SQ(ord(alpha_move[2]) - ord('a'), ord(alpha_move[3]) - ord('1'))
        
        _assert_condition(SqOnBoard(fromSq) and SqOnBoard(toSq))
        list = MOVELIST()
        list.generate_all_moves(board)
        Move = MOVE.NOMOVE
        PromPce = Pieces.EMPTY
        
        for MoveNum in range(0, list.count): # traversing the move list
            Move = list.moves[MoveNum] # getting the move of MOVE()
            if(Move.FROMSQ() == fromSq and Move.TOSQ() == toSq): # if both the to and from sqaures are same, then move is also same, provided promoted piece can be different
                PromPce = Move.PROMOTED()
                if(PromPce != Pieces.EMPTY): # if there is a promotion, we need to check
                    if(PieceRookQueen[PromPce] and not PieceBishopQueen[PromPce] and alpha_move[4] == 'r'): # promoted piece is a rook
                        return Move
                    elif(not PieceRookQueen[PromPce] and PieceBishopQueen[PromPce] and alpha_move[4] == 'b'): # promoted piece is bishop
                        return Move
                    elif(PieceBishopQueen[PromPce] and PieceRookQueen[PromPce] and alpha_move[4] == 'q'): #is a queen
                        return Move
                    elif(PieceKnight[PromPce] and alpha_move[4] == 'n'): 
                        return Move
                    continue
                return Move # else , if there was no promotion, then indeed move has matched, 
        
        return MOVE.NOMOVE # if we didn't found the move in movelist
    
MOVE.NOMOVE = MOVE()
    
class MOVELIST:
    """
    A class representing a list of chess moves. This class stores a collection of MOVE objects and keeps track of the 
    total number of moves in the list.

    Attributes:
        moves (list): A list of MOVE objects, initialized with a maximum capacity of 256.
        count (int): The total number of moves currently in the list.

    """
    def __init__(self):
        self.moves = [MOVE() for _ in range(256)]
        self.count = 0
        
    def _add_quite_move(self, board, move: MOVE) -> None:
        """
        Adds a quite move (non-capture) to the move list with an associated score, considering killer and history heuristics.
        
        Args:
            board (Board): The current state of the chess board.
            move (MOVE): The move object to be added to the move list.
        """
        _assert_condition(SqOnBoard(move.FROMSQ()))
        _assert_condition(SqOnBoard(move.TOSQ()))
        self.moves[self.count] = move
        self.moves[self.count].score = 0
        if(board.searchKillers[0][board.ply].move == move.move):
            self.moves[self.count].score = 900000
        elif (board.searchKillers[1][board.ply].move == move.move):
            self.moves[self.count].score = 800000
        else:
            self.moves[self.count].score = board.searchHistory[board.pieces[move.FROMSQ()]][move.TOSQ()].score
        self.count += 1
        
    def _add_capture_move(self, board, move: MOVE) -> None:
        """
        Adds a capture move to the move list, with a score based on the captured and attacking pieces.

        Args:
            board(Board): The current state of the chess board.
            move (MOVE): The capture move to be added to the move list.
        """
        _assert_condition(SqOnBoard(move.FROMSQ()))
        _assert_condition(SqOnBoard(move.TOSQ()))
        _assert_condition(PieceValid(move.CAPTURED()))
        self.moves[self.count] = move
        self.moves[self.count].score = MvvLvaScores[move.CAPTURED()][board.pieces[move.FROMSQ()]] + 1000000 # victim , attacker
        self.count += 1
        
    def _add_enpas_move(self, board, move: MOVE) -> None:
        """
        Adds an en passant move to the move list with a predefined score.

        Args:
            board (Board): The current state of the chess board.
            move (MOVE): The en passant move to be added to the move list.
        """
        _assert_condition(SqOnBoard(move.FROMSQ()))
        _assert_condition(SqOnBoard(move.TOSQ()))
        self.moves[self.count] = move
        self.moves[self.count].score = 105 + 1000000 # pawn takes pawn
        self.count += 1
        
    def _add_white_pawn_cap_move(self, board, from_square: int, to_square: int, cap: int) -> None:
        _assert_condition(SqOnBoard(from_square))
        _assert_condition(SqOnBoard(to_square))
        _assert_condition(PieceValidEmpty(cap))
        
        if(RanksBrd[from_square] == Ranks.R7): # if a white pawn captures something from rank 7, then it is promotion move
            self._add_capture_move(board, MOVE(from_square, to_square,cap,Pieces.wQ, 0)) # promoted to white Queen
            self._add_capture_move(board, MOVE(from_square, to_square,cap,Pieces.wR, 0)) # promoted to white Rook
            self._add_capture_move(board, MOVE(from_square, to_square,cap,Pieces.wB, 0)) # promoted to white Bishop
            self._add_capture_move(board, MOVE(from_square, to_square,cap,Pieces.wN, 0)) # promoted to white Knight
        else: # if it is not an promotion move
            self._add_capture_move(board, MOVE(from_square, to_square, cap, Pieces.EMPTY, 0))
            
    def _add_white_pawn_move(self, board, from_square: int, to_square: int) -> None: # same as above, the difference is it doesn't capture any piece
        _assert_condition(SqOnBoard(from_square))
        _assert_condition(SqOnBoard(to_square))
        if(RanksBrd[from_square] == Ranks.R7): # if a white pawn captures something from rank 7, then it is promotion move
            self._add_quite_move(board, MOVE(from_square, to_square,Pieces.EMPTY,Pieces.wQ, 0)) # promoted to white Queen
            self._add_quite_move(board, MOVE(from_square, to_square,Pieces.EMPTY,Pieces.wR, 0)) # promoted to white Rook
            self._add_quite_move(board, MOVE(from_square, to_square,Pieces.EMPTY,Pieces.wB, 0)) # promoted to white Bishop
            self._add_quite_move(board, MOVE(from_square, to_square,Pieces.EMPTY,Pieces.wN, 0)) # promoted to white Knight
        else: # if it is not an promotion move
            self._add_quite_move(board, MOVE(from_square, to_square, Pieces.EMPTY, Pieces.EMPTY, 0))
            
    def _add_black_pawn_cap_move(self, board, from_square: int, to_square: int, cap: int) -> None:
        _assert_condition(SqOnBoard(from_square))
        _assert_condition(SqOnBoard(to_square))
        _assert_condition(PieceValidEmpty(cap))
        if(RanksBrd[from_square] == Ranks.R2): # if a black pawn captures something from rank 2, then it is promotion move
            self._add_capture_move(board, MOVE(from_square, to_square,cap,Pieces.bQ, 0)) # promoted to black Queen
            self._add_capture_move(board, MOVE(from_square, to_square,cap,Pieces.bR, 0)) # promoted to black Rook
            self._add_capture_move(board, MOVE(from_square, to_square,cap,Pieces.bB, 0)) # promoted to black Bishop
            self._add_capture_move(board, MOVE(from_square, to_square,cap,Pieces.bN, 0)) # promoted to black Knight
        else: # if it is not an promotion move
            self._add_capture_move(board, MOVE(from_square, to_square, cap, Pieces.EMPTY, 0))
            
    def _add_black_pawn_move(self, board, from_square: int, to_square: int) -> None:
        _assert_condition(SqOnBoard(from_square))
        _assert_condition(SqOnBoard(to_square))
        if(RanksBrd[from_square] == Ranks.R2): # if a Black pawn captures something from rank 2, then it is promotion move
            self._add_quite_move(board, MOVE(from_square, to_square,Pieces.EMPTY,Pieces.bQ, 0)) # promoted to Black Queen
            self._add_quite_move(board, MOVE(from_square, to_square,Pieces.EMPTY,Pieces.bR, 0)) # promoted to Black Rook
            self._add_quite_move(board, MOVE(from_square, to_square,Pieces.EMPTY,Pieces.bB, 0)) # promoted to Black Bishop
            self._add_quite_move(board, MOVE(from_square, to_square,Pieces.EMPTY,Pieces.bN, 0)) # promoted to Black Knight
        else: # if it is not an promotion move
            self._add_quite_move(board, MOVE(from_square, to_square, Pieces.EMPTY, Pieces.EMPTY, 0))
        
    def generate_all_moves(self, board) -> None:
        """
        Generates a list of all legal moves for the current side in a given board state.
        
        This method processes the position based on the current side (White or Black) and adds all 
        possible legal moves to a move list, taking into account piece types and board conditions. 
    
        """
        _assert_condition(board._check_board())
    
        # generating white pawn moves
        self.count = 0
        pce = Pieces.EMPTY
        side = board.side
        sq = 0
        t_sq = 0
        
        if(side == Colors.WHITE):
            # looping to total number of white pawns on the board
            for pceNum in range(0, board.pceNum[Pieces.wP]):
                sq = board.pList[Pieces.wP][pceNum] # to get the square on which there is a white Pawn
                _assert_condition(SqOnBoard(sq))
                
                # if it is a no capture move
                if(board.pieces[sq + 10] == Pieces.EMPTY):
                    self._add_white_pawn_move(board, sq, sq+10) # board, fromSq, ToSq
                    
                    if(RanksBrd[sq] == Ranks.R2 and board.pieces[sq + 20] == Pieces.EMPTY):
                        self._add_quite_move(board, MOVE(sq, sq+20, Pieces.EMPTY, Pieces.EMPTY, MOVE.FLAG_PS)) # added a quite move, because there was no capture, also setted the Pawn Start Flag
                        
                # if it is a capture move            
                if(not SQOFFBOARD(sq + 9) and PieceCol[board.pieces[sq + 9]] == Colors.BLACK): # if the capturing piece is black
                    self._add_white_pawn_cap_move(board, sq, sq+9, board.pieces[sq+9]) # board, fromSq, ToSq, CapturedPiece
                    
                if(not SQOFFBOARD(sq + 11) and PieceCol[board.pieces[sq + 11]] == Colors.BLACK): # if the capturing piece is black
                    self._add_white_pawn_cap_move(board, sq, sq+11, board.pieces[sq+11]) # board, fromSq, ToSq, CapturedPiece
                if(board.enPas != Squares.NO_SQ):
                    if(sq + 9 == board.enPas):
                        self._add_enpas_move(board, MOVE(sq, sq+9, Pieces.EMPTY, Pieces.EMPTY, MOVE.FLAG_EP))
                    if(sq + 11 == board.enPas):
                        self._add_enpas_move(board, MOVE(sq, sq+11, Pieces.EMPTY, Pieces.EMPTY, MOVE.FLAG_EP))
                    
            # castling for white
            # king side castling
            if(board.castlePerm & Castling.WKCA): #if white can castle king side
                if(board.pieces[Squares.F1] == Pieces.EMPTY and board.pieces[Squares.G1] == Pieces.EMPTY): # if between the king and rook squares are empty
                    if(not is_sqaure_attacked(Squares.E1, Colors.BLACK, board) and not is_sqaure_attacked(Squares.F1, Colors.BLACK, board)): # if the square F1, E1 are not attacked, only then king can castle, beacause, king cannot castle in between check
                        
                        # adding the castle move white king side castle
                        self._add_quite_move(board, MOVE(Squares.E1, Squares.G1, Pieces.EMPTY, Pieces.EMPTY, MOVE.FLAG_CA))
                        
            if(board.castlePerm & Castling.WQCA):
                if(board.pieces[Squares.D1] == Pieces.EMPTY and board.pieces[Squares.C1] == Pieces.EMPTY and board.pieces[Squares.B1] == Pieces.EMPTY): # if between the king and rook squares are empty
                    if(not is_sqaure_attacked(Squares.E1, Colors.BLACK, board) and not is_sqaure_attacked(Squares.D1, Colors.BLACK, board)): # if the square D1, E1 are not attacked, only then king can castle, beacause, king cannot castle in between check
                        
                        # adding the castle move white queen side castle
                        self._add_quite_move(board, MOVE(Squares.E1, Squares.C1, Pieces.EMPTY, Pieces.EMPTY, MOVE.FLAG_CA))
        else: 
            # looping to total number of black pawns on the board
            for pceNum in range(0, board.pceNum[Pieces.bP]):
                sq = board.pList[Pieces.bP][pceNum] # to get the square on which there is a black Pawn
                _assert_condition(SqOnBoard(sq))
                
                # if it is a no capture move
                if(board.pieces[sq - 10] == Pieces.EMPTY):
                    self._add_black_pawn_move(board, sq, sq-10) # board, fromSq, ToSq
                    #
                    if(RanksBrd[sq] == Ranks.R7 and board.pieces[sq - 20] == Pieces.EMPTY):
                        self._add_quite_move(board, MOVE(sq, sq-20, Pieces.EMPTY, Pieces.EMPTY, MOVE.FLAG_PS)) # added a quite move, because there was no capture, also setted the Pawn Start Flag
                        
                # if it is a capture move            
                if(not SQOFFBOARD(sq - 9) and PieceCol[board.pieces[sq - 9]] == Colors.WHITE): # if the capturing piece is WHITE
                    self._add_black_pawn_cap_move(board, sq, sq-9, board.pieces[sq-9]) # board, fromSq, ToSq, CapturedPiece
                    
                if(not SQOFFBOARD(sq - 11) and PieceCol[board.pieces[sq - 11]] == Colors.WHITE): # if the capturing piece is WHITE
                    self._add_black_pawn_cap_move(board, sq, sq-11, board.pieces[sq-11]) # board, fromSq, ToSq, CapturedPiece
                if(board.enPas != Squares.NO_SQ):
                    if(sq - 9 == board.enPas):
                        self._add_enpas_move(board, MOVE(sq, sq-9, Pieces.EMPTY, Pieces.EMPTY, MOVE.FLAG_EP))
                    if(sq - 11 == board.enPas):
                        self._add_enpas_move(board, MOVE(sq, sq-11, Pieces.EMPTY, Pieces.EMPTY, MOVE.FLAG_EP))
                    
            # castling for black
            # king side castling
            if(board.castlePerm & Castling.BKCA):
                if(board.pieces[Squares.F8] == Pieces.EMPTY and board.pieces[Squares.G8] == Pieces.EMPTY): # if between the king and rook squares are empty
                    if(not is_sqaure_attacked(Squares.E8, Colors.WHITE, board) and not is_sqaure_attacked(Squares.F8, Colors.WHITE, board)): # if the square F8, E8 are not attacked, only then king can castle, beacause, king cannot castle in between check
                        
                        # adding the castle move black king side castle
                        self._add_quite_move(board, MOVE(Squares.E8, Squares.G8, Pieces.EMPTY, Pieces.EMPTY, MOVE.FLAG_CA))
                        
            if(board.castlePerm & Castling.BQCA):
                if(board.pieces[Squares.D8] == Pieces.EMPTY and board.pieces[Squares.C8] == Pieces.EMPTY and board.pieces[Squares.B8] == Pieces.EMPTY): # if between the king and rook squares are empty
                    if(not is_sqaure_attacked(Squares.E8, Colors.WHITE, board) and not is_sqaure_attacked(Squares.D8, Colors.WHITE, board)): # if the square D8, E8 are not attacked, only then king can castle, beacause, king cannot castle in between check
                        
                        # adding the castle move black queen side castle
                        self._add_quite_move(board, MOVE(Squares.E8, Squares.C8, Pieces.EMPTY, Pieces.EMPTY, MOVE.FLAG_CA))

        # Move generation for sliding pieces (Bishops, Rooks, Queen)
        pceIndex = LoopSlideIndex[side] # WHITE - 0, BLACK - 4
        pce = LoopSlidePce[pceIndex] # for white First piece is White Bishop
        
        while(pce != 0):
            _assert_condition(PieceValid(pce))
            pce = LoopSlidePce[pceIndex]
            for pceNum in range(0, board.pceNum[pce]):
                sq = board.pList[pce][pceNum] # accesing the square on which that particular piece is
                _assert_condition(SqOnBoard(sq))
                
                #generating the moves
                for index in range(NumDir[pce]): # looping till no of directions for each piece
                    dir = PceDir[pce][index]
                    t_sq = sq + dir
                    
                    while(not SQOFFBOARD(t_sq)):   # for sliding pieces we need to iterate in that direction till we are offboard 
                        # capture move, BLACK(1) ^ 1 == WHITE(0)
                        if(board.pieces[t_sq] != Pieces.EMPTY):
                            if(PieceCol[board.pieces[t_sq]] == side ^ 1): # opposite color
                                
                                # addding a capture move
                                self._add_capture_move(board, MOVE(sq, t_sq, board.pieces[t_sq], Pieces.EMPTY, 0))
                                
                            break #if same color piece is found then break, we can't move further
                        
                        # Normal Move
                        self._add_quite_move(board, MOVE(sq, t_sq, Pieces.EMPTY, Pieces.EMPTY, 0))
                        t_sq += dir
            
            pceIndex += 1
        
        
        # Move generation for non sliding pieces (Knights, King)
        pceIndex = LoopNonSlideIndex[side] # WHITE - 0, BLACK - 4
        pce = LoopNonSlidePce[pceIndex] # for white First piece is White Knight
        
        while(pce != 0):
            _assert_condition(PieceValid(pce))
            pce = LoopNonSlidePce[pceIndex]
            
            for pceNum in range(0, board.pceNum[pce]):
                sq = board.pList[pce][pceNum] # accesing the square on which that particular piece is
                _assert_condition(SqOnBoard(sq))
                
                #generating the moves
                for index in range(NumDir[pce]): # looping till no of directions for each piece
                    dir = PceDir[pce][index]
                    t_sq = sq + dir
                    if(SQOFFBOARD(t_sq)):
                        continue
                    
                    # capture move, BLACK(1) ^ 1 == WHITE(0)
                    if(board.pieces[t_sq] != Pieces.EMPTY):
                        if(PieceCol[board.pieces[t_sq]] == side ^ 1): # opposite color
                            # addding a capture move
                            self._add_capture_move(board, MOVE(sq, t_sq, board.pieces[t_sq], Pieces.EMPTY, 0))
                        continue #if same color then skip
                    
                    # Normal Move
                    self._add_quite_move(board, MOVE(sq, t_sq, Pieces.EMPTY, Pieces.EMPTY, 0))
            
            pceIndex += 1
            
    def _generate_capture_moves(self, board) -> None:
        """
        Generates a list of all legal **capture** moves for the current side in a given board state.
        
        This method processes the position based on the current side (White or Black) and adds all 
        possible legal capture moves to a move list, taking into account piece types and board conditions. 
    
        """
        _assert_condition(board._check_board())
        
        # generating white pawn moves
        self.count = 0
        pce = Pieces.EMPTY
        side = board.side
        sq = 0
        t_sq = 0
        
        if(side == Colors.WHITE):
            # looping to total number of white pawns on the board
            for pceNum in range(0, board.pceNum[Pieces.wP]):
                sq = board.pList[Pieces.wP][pceNum] # to get the square on which there is a white Pawn
                _assert_condition(SqOnBoard(sq))
                                    
                # if it is a capture move            
                if(not SQOFFBOARD(sq + 9) and PieceCol[board.pieces[sq + 9]] == Colors.BLACK): # if the capturing piece is black
                    self._add_white_pawn_cap_move(board, sq, sq+9, board.pieces[sq+9]) # board, fromSq, ToSq, CapturedPiece, list
                    
                if(not SQOFFBOARD(sq + 11) and PieceCol[board.pieces[sq + 11]] == Colors.BLACK): # if the capturing piece is black
                    self._add_white_pawn_cap_move(board, sq, sq+11, board.pieces[sq+11]) # board, fromSq, ToSq, CapturedPiece, list
                if(board.enPas != Squares.NO_SQ):
                    if(sq + 9 == board.enPas):
                        self._add_enpas_move(board, MOVE(sq, sq+9, Pieces.EMPTY, Pieces.EMPTY, MOVE.FLAG_EP))
                    if(sq + 11 == board.enPas):
                        self._add_enpas_move(board, MOVE(sq, sq+11, Pieces.EMPTY, Pieces.EMPTY, MOVE.FLAG_EP))
                    

        else: 
            # looping to total number of black pawns on the board
            for pceNum in range(0, board.pceNum[Pieces.bP]):
                sq = board.pList[Pieces.bP][pceNum] # to get the square on which there is a black Pawn
                _assert_condition(SqOnBoard(sq))
                        
                # if it is a capture move            
                if(not SQOFFBOARD(sq - 9) and PieceCol[board.pieces[sq - 9]] == Colors.WHITE): # if the capturing piece is WHITE
                    self._add_black_pawn_cap_move(board, sq, sq-9, board.pieces[sq-9]) # board, fromSq, ToSq, CapturedPiece, list
                    
                if(not SQOFFBOARD(sq - 11) and PieceCol[board.pieces[sq - 11]] == Colors.WHITE): # if the capturing piece is WHITE
                    self._add_black_pawn_cap_move(board, sq, sq-11, board.pieces[sq-11]) # board, fromSq, ToSq, CapturedPiece, list
                if(board.enPas != Squares.NO_SQ):
                    if(sq - 9 == board.enPas):
                        self._add_enpas_move(board, MOVE(sq, sq-9, Pieces.EMPTY, Pieces.EMPTY, MOVE.FLAG_EP))
                    if(sq - 11 == board.enPas):
                        self._add_enpas_move(board, MOVE(sq, sq-11, Pieces.EMPTY, Pieces.EMPTY, MOVE.FLAG_EP))
                    
        # Move generation for sliding pieces (Bishops, Rooks, Queen)
        pceIndex = LoopSlideIndex[side] # WHITE - 0, BLACK - 4
        pce = LoopSlidePce[pceIndex] # for white First piece is White Bishop
        
        while(pce != 0):
            _assert_condition(PieceValid(pce))
            pce = LoopSlidePce[pceIndex]
            for pceNum in range(0, board.pceNum[pce]):
                sq = board.pList[pce][pceNum] # accesing the square on which that particular piece is
                _assert_condition(SqOnBoard(sq))
                
                #generating the moves
                for index in range(NumDir[pce]): # looping till no of directions for each piece
                    dir = PceDir[pce][index]
                    t_sq = sq + dir
                    
                    while(not SQOFFBOARD(t_sq)):   # for sliding pieces we need to iterate in that direction till we are offboard 
                        # capture move, BLACK(1) ^ 1 == WHITE(0)
                        if(board.pieces[t_sq] != Pieces.EMPTY):
                            if(PieceCol[board.pieces[t_sq]] == side ^ 1): # opposite color
                                
                                # addding a capture move
                                self._add_capture_move(board, MOVE(sq, t_sq, board.pieces[t_sq], Pieces.EMPTY, 0))
                                
                            break #if same color piece is found then break, we can't move further
                        
                        # Normal Move

                        t_sq += dir
            
            pceIndex += 1
        
        
        # Move generation for non sliding pieces (Knights, King)
        pceIndex = LoopNonSlideIndex[side] # WHITE - 0, BLACK - 4
        pce = LoopNonSlidePce[pceIndex] # for white First piece is White Knight
        
        while(pce != 0):
            _assert_condition(PieceValid(pce))
            pce = LoopNonSlidePce[pceIndex]
            
            for pceNum in range(0, board.pceNum[pce]):
                sq = board.pList[pce][pceNum] # accesing the square on which that particular piece is
                _assert_condition(SqOnBoard(sq))
                
                #generating the moves
                for index in range(NumDir[pce]): # looping till no of directions for each piece
                    dir = PceDir[pce][index]
                    t_sq = sq + dir
                    if(SQOFFBOARD(t_sq)):
                        continue
                    
                    # capture move, BLACK(1) ^ 1 == WHITE(0)
                    if(board.pieces[t_sq] != Pieces.EMPTY):
                        if(PieceCol[board.pieces[t_sq]] == side ^ 1): # opposite color
                            # addding a capture move
                            self._add_capture_move(board, MOVE(sq, t_sq, board.pieces[t_sq], Pieces.EMPTY, 0))
                        continue #if same color then skip
                    
                    # Normal Move
            
            pceIndex += 1

    def _get_move_list(self) -> list:
        """
        Returns a list of moves in algebraic notation for all currently generated moves.

        This method maps each move in the `moves` array to its algebraic notation by calling 
        the `alpha_move` method on each move.
        
        Returns:
            list[str]: A list of move strings in algebraic notation format.
        """
        return list(map(lambda move: move.alpha_move(), self.moves[:self.count])) 
    
    def print_move_list(self) -> None:
        """
        Prints the move list
        
        """
        print("Move List: ")
        for i in range(0, self.count):
            move = self.moves[i]
            score = self.moves[i].score
            
            print(f"Move: {i+1} --> {move.alpha_move()} (Score: {score})")
        print(f"Move List Total {self.count} Moves: \n")
        
    def _pick_next_move(self, movenum: int) -> None:
        """
        Prioritizes the most promising move by iterating through available moves 
        and selecting the one with the highest score, starting from the specified 
        index `movenum`. The highest-scoring move is then swapped with the move at 
        `movenum`, ensuring it is evaluated first in AlphaBeta pruning. This move 
        ordering improves pruning efficiency by increasing the likelihood of 
        encountering cutoffs earlier in the search.

        Args:
            movenum (int): The index from which to start evaluating moves.
        """
        bestScore = 0
        bestNum = movenum
        for index in range(movenum, self.count): # from given moveNum to end of movelist
            if(self.moves[index].score > bestScore):
                bestScore = self.moves[index].score
                bestNum = index
        # swapping it (move ordering)    
        self.moves[movenum], self.moves[bestNum] = self.moves[bestNum], self.moves[movenum]