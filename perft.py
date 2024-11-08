from board import Board
from debug import assert_condition
from misc import GetTimeMs
from move import MOVELIST

leafNodes = 0

def Perft(depth, board: Board):
    global leafNodes
    assert_condition(board.check_board())
    
    if(depth == 0):
        leafNodes += 1
        return 
    
    list = MOVELIST()
    list.generate_all_moves(board)
    
    for MoveNum in range(0, list.count):
        if(not board.make_move(list.moves[MoveNum].move)):
            continue
        Perft(depth - 1, board)
        board.take_move()
    
    return 

def PerftTest(depth, board: Board):
    global leafNodes
    assert_condition(board.check_board())
    
    board.print_board()
    
    print(f"\nStarting Test to Depth: {depth}")
    leafNodes = 0
    start = GetTimeMs()
    
    list = MOVELIST()
    list.generate_all_moves(board)
    
    for MoveNum in range(0 , list.count):
        move = list.moves[MoveNum].move
        if(not board.make_move(move)):
            continue
        
        cumnodes = leafNodes
        Perft(depth - 1, board)
        board.take_move()
        oldnodes = leafNodes - cumnodes
        print(f"Move {MoveNum+1} is {move.alpha_move()} : {oldnodes}")
    
    print(f"Test Complete: {leafNodes} nodes visited in {GetTimeMs() - start}ms\n")
    return