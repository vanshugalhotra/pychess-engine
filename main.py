import constants
import init
from bitboards import PrintBitBoard
from board import ParseFen, PrintBoard,CheckBoard
from debug import assert_condition
from movegen import PAWNS_B, PAWNS_W, KNIGHTSKINGS,CASTLE1, CASTLE2, TRICKY, GenerateAllMoves
from input_output import PrintMoveList, PrMove, parseMove
from makemove import MakeMove, TakeMove
from perft import PerftTest

PERFTFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 "

if __name__ == "__main__":
    init.AllInit()
    boardR = constants.Board()
    
    ParseFen(PERFTFEN, boardR)
    # PerftTest(3, boardR)
    Move = 0
    
    while(True):
        PrintBoard(boardR)
        mo = input("Please Enter a Move: ")
        if(mo[0] == 'q'):
            break
        elif(mo[0] == 't'):
            TakeMove(boardR)
        else:
            Move = parseMove(mo, boardR)
            if(Move != 0):
                MakeMove(boardR, Move)
            else:
                print("INVALID")
    

        
    
    