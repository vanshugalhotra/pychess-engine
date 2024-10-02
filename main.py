import constants
import init
from bitboards import PrintBitBoard
from board import ParseFen, PrintBoard,CheckBoard
from debug import assert_condition
from movegen import PAWNS_B, PAWNS_W, KNIGHTSKINGS,CASTLE1, CASTLE2, TRICKY, GenerateAllMoves
from input_output import PrintMoveList, PrMove
from makemove import MakeMove, TakeMove
from perft import PerftTest

PERFTFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 "

if __name__ == "__main__":
    init.AllInit()
    boardR = constants.Board()
    
    ParseFen(PERFTFEN, boardR)
    PerftTest(3, boardR)
    

        
    
    