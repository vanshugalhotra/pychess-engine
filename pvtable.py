import sys
from constants import MAXDEPTH
from debug import assert_condition
from move import MOVE

NOMOVE = 0

class PVENTRY:
    def __init__(self):
        self.posKey = 0
        self.move = MOVE()

class PVTABLE:
    def __init__(self):
        self.numEntries = 0
        self.pTable = [] # to store the entry of PVENTRY

def sizeof(cls):
    return sys.getsizeof(cls())

PvSize = 0x10000 * 2  # (2 MB)
MAXPVENTRIES = 131072

def ClearPvTable(table):
    for i in range(0, table.numEntries):
        table.pTable[i].posKey = 0
        table.pTable[i].move = NOMOVE

def InitPvTable(table):
    # table.numEntries = PvSize // sizeof(PVENTRY)
    table.numEntries = MAXPVENTRIES
    table.numEntries -= 2
    
    for _ in range(0, table.numEntries):
        table.pTable.append(PVENTRY())
        
    ClearPvTable(table)
        
    print(f"PvTable init complete with {table.numEntries} entries")
    
def StorePvMove(board, move: MOVE):
    index = board.posKey % board.PvTable.numEntries
    assert_condition(index >=0 and index <= board.PvTable.numEntries-1)
    
    board.PvTable.pTable[index].move = move
    board.PvTable.pTable[index].posKey = board.posKey
    
def ProbePvTable(board):
    index = board.posKey % board.PvTable.numEntries
    assert_condition(index >=0 and index <= board.PvTable.numEntries-1)
    
    if(board.PvTable.pTable[index].posKey == board.posKey):
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
    