import constants
import init
from bitboards import PrintBitBoard
from board import ParseFen, PrintBoard,CheckBoard
from debug import assert_condition

if __name__ == "__main__":
    init.AllInit()
    boardR = constants.Board()
    
    ParseFen(constants.FEN4, boardR)
    PrintBoard(boardR)
    
    assert_condition(CheckBoard(boardR))
    
    
    