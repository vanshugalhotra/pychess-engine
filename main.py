import constants
import init
from board import ParseFen, PrintBoard
from input_output import parseMove, PrMove
from makemove import MakeMove, TakeMove
from perft import PerftTest
from pvtable import StorePvMove, GetPvLine

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
        elif(mo[0] == 'p'):
            PerftTest(int(mo[1]), boardR)
        elif(mo[0] == 'v'):
            Max = GetPvLine(4, boardR)
            print(f"PvLine of {Max} Moves: ")
            for PvNum in range(Max):
                Move = boardR.PvArray[PvNum]
                print(PrMove(Move))
        else:
            Move = parseMove(mo, boardR)
            if(Move != 0):
                StorePvMove(boardR, Move)
                MakeMove(boardR, Move)

            else:
                print("INVALID")
    

        
    
    