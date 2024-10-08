import sys
from constants import PVENTRY

NOMOVE = 0

def sizeof(cls):
    return sys.getsizeof(cls())

PvSize = 0x10000 * 2  # (2 MB)
MAXPVENTRIES = 130000

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