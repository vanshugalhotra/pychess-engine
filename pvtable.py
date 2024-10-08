import sys
from constants import PVENTRY
from debug import assert_condition

NOMOVE = 0

def sizeof(cls):
    return sys.getsizeof(cls())

PvSize = 0x10000 * 2  # (2 MB)
MAXPVENTRIES = 130780

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
    
def StorePvMove(board, move):
    index = board.posKey % board.PvTable.numEntries
    assert_condition(index >=0 and index <= board.PvTable.numEntries-1)
    
    board.PvTable.pTable[index].move = move
    board.PvTable.pTable[index].posKey = board.posKey
    
def ProbePvTable(board):
    index = board.posKey % board.PvTable.numEntries
    assert_condition(index >=0 and index <= board.PvTable.numEntries-1)
    
    if(board.PvTable.pTable[index].posKey == board.posKey):
        return board.PvTable.pTable[index].move
    return NOMOVE
    
    