import constants
import init
from bitboards import PrintBitBoard
from board import ParseFen, PrintBoard,CheckBoard
from debug import assert_condition
from movegen import PAWNS_B, PAWNS_W, KNIGHTSKINGS,CASTLE1, CASTLE2, TRICKY, GenerateAllMoves
from input_output import PrintMoveList, PrMove
from makemove import MakeMove, TakeMove

if __name__ == "__main__":
    init.AllInit()
    boardR = constants.Board()
    
    ParseFen(constants.START_FEN, boardR)
    movelist = constants.MOVELIST()
    
    GenerateAllMoves(boardR, movelist)
    
    move = 0
    PrintBoard(boardR)
    CheckBoard(boardR)
    input()
    for MoveNum in range(0, movelist.count):
        move = movelist.moves[MoveNum].move
        if(not MakeMove(boardR, move)):
            continue
        
        print(f"\nMade: {PrMove(move)}")
        PrintBoard(boardR)
        
        TakeMove(boardR)
        
        print(f"\nTaken: {PrMove(move)}")
        # PrintBoard(boardR)
        
        input()
        
    
    