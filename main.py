import constants
import init
from board import ParseFen, PrintBoard
from input_output import parseMove, PrMove
from makemove import MakeMove, TakeMove
from perft import PerftTest
from pvtable import StorePvMove, InitPvTable
from search import SearchPosition

PERFTFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 "
WAC1 = "2rr3k/pp3pp1/1nnqbN1p/3pN3/2pP4/2P3Q1/PPB4P/R4RK1 w - -"
WAC2 = "r1b1k2r/ppppnppp/2n2q2/2b5/3NP3/2P1B3/PP3PPP/RN1QKB1R w KQkq - 0 1"

if __name__ == "__main__":
    init.AllInit()
    boardR = constants.Board()
        
    InitPvTable(boardR.PvTable)
    
    info = constants.SEARCHINFO()
    
    ParseFen(WAC2, boardR)
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
        elif(mo[0] == 's'):
            info.depth = 5
            SearchPosition(boardR, info)
        else:
            Move = parseMove(mo, boardR)
            if(Move != 0):
                StorePvMove(boardR, Move)
                MakeMove(boardR, Move)

            else:
                print("INVALID")
    

        
    
    