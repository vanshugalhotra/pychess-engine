from pychess_engine.board import Board
from pychess_engine.debug import _assert_condition
from pychess_engine.move import MOVELIST
from pychess_engine.helper import execution_time

leafNodes = 0

def Perft(depth, board: Board):
    global leafNodes
    _assert_condition(board._check_board())
    
    if(depth == 0):
        leafNodes += 1
        return 
    
    list = MOVELIST()
    list.generate_all_moves(board)
    
    for MoveNum in range(0, list.count):
        if(not board.make_move(list.moves[MoveNum])):
            continue
        Perft(depth - 1, board)
        board.take_move()
    
    return 

@execution_time
def PerftTest(depth, board: Board):
    global leafNodes
    _assert_condition(board._check_board())
    
    board.print_board()
    
    print(f"\nStarting Test to Depth: {depth}")
    leafNodes = 0

    list = MOVELIST()
    list.generate_all_moves(board)
    
    for MoveNum in range(0 , list.count):
        move = list.moves[MoveNum]
        if(not board.make_move(move)):
            continue
        
        cumnodes = leafNodes
        Perft(depth - 1, board)
        board.take_move()
        oldnodes = leafNodes - cumnodes
        print(f"Move {MoveNum+1} is {move.alpha_move()} : {oldnodes}")
    
    print(f"Test Complete: {leafNodes} nodes")
    return