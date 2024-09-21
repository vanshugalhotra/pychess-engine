import constants
import init
from bitboards import PrintBitBoard
from board import ParseFen, PrintBoard, UpdateListsMaterial

if __name__ == "__main__":
    init.AllInit()
    boardR = constants.Board()
    
    ParseFen(constants.FEN4, boardR)
    PrintBoard(boardR)
    PrintBitBoard(boardR.pawns[2])
    
    
    