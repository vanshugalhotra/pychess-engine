from constants import MAXDEPTH
from debug import assert_condition
from move import MOVE
from hashkeys import PositionKey

NOMOVE = 0
MAXPVENTRIES = 131072


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
        
    def clear_table(self) -> None:
        for i in range(0, self.numEntries):
            self.pTable[i].posKey = PositionKey()
            self.pTable[i].move = NOMOVE
            
    def store_pv_move(self, board, move: MOVE) -> None:
        index = board.posKey.key % self.numEntries
        assert_condition(index >=0 and index <= self.numEntries-1)

        self.pTable[index].move = move
        self.pTable[index].posKey.key = board.posKey.key
        
    def probe_pv_table(self, board) -> MOVE:
        index = board.posKey.key % self.numEntries
        assert_condition(index >=0 and index <= self.numEntries-1)

        if(self.pTable[index].posKey.key == board.posKey.key):
            return self.pTable[index].move
        return MOVE()
    
    def get_pv_line(self, board, depth: int) -> int:
        assert_condition(depth < MAXDEPTH)
    
        move_obj = self.probe_pv_table(board=board) # instance of MOVE()
        count = 0
        while(move_obj.move != NOMOVE and count < depth):
            assert_condition(count < depth)
            if(move_obj.move_exists(board)): # legal move
                board.make_move(move_obj)
                board.PvArray[count] = move_obj
                count += 1
            else:
                break # we have encountered an illegeal move_obj
            move_obj = self.probe_pv_table(board=board)
            
        while(board.ply > 0):
            board.take_move()
            
        return count

    