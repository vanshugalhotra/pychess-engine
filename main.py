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

def isRepetition(board):
    for index in range(board.hisPly - board.fiftyMove, board.hisPly-1): # checking from only when last time fiftyMove was set to 0 because once fifty move is set to 0 there won't be no repetetions(captures and pawn moves cant repeat)
        if(board.posKey == board.history[index].posKey):
            return True
        
    return False

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
                if(isRepetition(boardR)):
                    print("REPETETION FOUND!!")
            else:
                print("INVALID")
    

        
    
    