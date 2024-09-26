import constants
import init
from bitboards import PrintBitBoard
from board import ParseFen, PrintBoard,CheckBoard
from debug import assert_condition
from movegen import TEST_FEN, GenerateAllMoves
from input_output import PrintMoveList

if __name__ == "__main__":
    init.AllInit()
    boardR = constants.Board()
    
    ParseFen(TEST_FEN, boardR)
    PrintBoard(boardR)
    assert_condition(CheckBoard(boardR))
    
    movelist = constants.MOVELIST()
    GenerateAllMoves(boardR, movelist)
    PrintMoveList(movelist)
    
    
    
    