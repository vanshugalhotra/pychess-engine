import constants
import init
import bitboards
from board import ParseFen, PrintBoard

if __name__ == "__main__":
    init.AllInit()
    boardR = constants.Board()
    
    ParseFen(constants.FEN3, boardR)
    PrintBoard(boardR)