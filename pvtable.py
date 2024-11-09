from constants import MAXDEPTH
from debug import assert_condition
from move import MOVE
from hashkeys import PositionKey

NOMOVE = 0

class PVENTRY:
    def __init__(self):
        self.posKey = PositionKey()
        self.move = MOVE()

class PVTABLE:
    def __init__(self):
        self.numEntries = MAXPVENTRIES - 2
        self.pTable = [PVENTRY() for _ in range(self.numEntries)] # to store the entry of PVENTRY
        self.clear_table()
        print(f"PvTable init complete with {self.numEntries} entries")
        
    def clear_table(self):
        for i in range(0, self.numEntries):
            self.pTable[i].posKey = PositionKey()
            self.pTable[i].move = NOMOVE

MAXPVENTRIES = 131072

def StorePvMove(board, move: MOVE):
    index = board.posKey.key % board.PvTable.numEntries
    assert_condition(index >=0 and index <= board.PvTable.numEntries-1)
    
    board.PvTable.pTable[index].move = move
    board.PvTable.pTable[index].posKey.key = board.posKey.key
    
def ProbePvTable(board):
    index = board.posKey.key % board.PvTable.numEntries
    assert_condition(index >=0 and index <= board.PvTable.numEntries-1)
    
    if(board.PvTable.pTable[index].posKey.key == board.posKey.key):
        return board.PvTable.pTable[index].move
    return MOVE()
    
    
def GetPvLine(depth, board):
    assert_condition(depth < MAXDEPTH)
    
    move_obj = ProbePvTable(board) # instance of MOVE()
    count = 0
    while(move_obj.move != NOMOVE and count < depth):
        assert_condition(count < depth)
        if(move_obj.move_exists(board)): # legal move
            board.make_move(move_obj)
            board.PvArray[count] = move_obj
            count += 1
        else:
            break # we have encountered an illegeal move_obj
        move_obj = ProbePvTable(board)
        
    while(board.ply > 0):
        board.take_move()
        
    return count
    