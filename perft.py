from board import CheckBoard, PrintBoard
from debug import assert_condition
from constants import MOVELIST
from movegen import GenerateAllMoves
from makemove import MakeMove, TakeMove
from input_output import PrMove

leafNodes = 0

def Perft(depth, board):
    global leafNodes
    assert_condition(CheckBoard(board))
    
    if(depth == 0):
        leafNodes += 1
        return 
    
    list = MOVELIST()
    GenerateAllMoves(board, list)
    
    for MoveNum in range(0, list.count):
        if(not MakeMove(board, list.moves[MoveNum].move)):
            continue
        Perft(depth - 1, board)
        TakeMove(board)
    
    return 

def PerftTest(depth, board):
    global leafNodes
    assert_condition(CheckBoard(board))
    
    PrintBoard(board)
    
    print(f"\nStarting Test to Depth: {depth}")
    leafNodes = 0
    
    list = MOVELIST()
    GenerateAllMoves(board, list)
    
    for MoveNum in range(0, list.count):
        move = list.moves[MoveNum].move
        if(not MakeMove(board, move)):
            continue
        
        cumnodes = leafNodes
        Perft(depth - 1, board)
        TakeMove(board)
        oldnodes = leafNodes - cumnodes
        print(f"Move {MoveNum+1} is {PrMove(move)} : {oldnodes}")
    
    print(f"Test Complete: {leafNodes} nodes visited\n")
    return