from constants import MAXDEPTH
from debug import _assert_condition
from move import MOVE
from hashkeys import PositionKey

MAXPVENTRIES = 131072

class PVENTRY:
    """
    Represents a Principal Variation Table (PVT) entry, used in storing moves 
    and position keys for a chess engine's principal variation path.

    Attributes:
        posKey (PositionKey): The unique key representing a board position.
        move (MOVE): The best move determined for the current position.
    """
    def __init__(self):
        self.posKey = PositionKey()
        self.move = MOVE()

class PVTABLE:
    """
    Represents a Principal Variation Table (PVT) to store optimal moves for positions in a chess engine.

    Attributes:
        numEntries (int): The number of entries available in the PVT.
        pTable (list): A list of `PVENTRY` objects storing moves and position keys.
    """
    def __init__(self):
        self.numEntries = MAXPVENTRIES - 2
        self.pTable = [PVENTRY() for _ in range(self.numEntries)] # to store the entry of PVENTRY
        self._clear_table()
        
    def _clear_table(self) -> None:
        """Clears the PVT by resetting all entries to empty states."""
        for i in range(0, self.numEntries):
            self.pTable[i].posKey = PositionKey()
            self.pTable[i].move = MOVE.NOMOVE
            
    def _store_pv_move(self, board, move: MOVE) -> None:
        """
        Stores a move in the PVT for a given board position.

        Args:
            board(Board): The board object containing the current position.
            move (MOVE): The move to store as the principal variation for the board position.
        """
        index = board.posKey.key % self.numEntries
        _assert_condition(index >=0 and index <= self.numEntries-1)

        self.pTable[index].move = move
        self.pTable[index].posKey.key = board.posKey.key
        
    def _probe_pv_table(self, board) -> MOVE:
        """
        Retrieves the stored principal variation move for a board position, if available.

        Args:
            board: The board object containing the current position.

        Returns:
            MOVE: The stored move if it matches the position key, or a default `MOVE` object if no match is found.
        """
        index = board.posKey.key % self.numEntries
        _assert_condition(index >=0 and index <= self.numEntries-1)

        if(self.pTable[index].posKey.key == board.posKey.key):
            return self.pTable[index].move
        return MOVE()
    
    def _get_pv_line(self, board, depth: int) -> int:
        """
        Generates the principal variation line up to a specified `depth` for a given board position.

        Args:
            board(Board): The board object containing the current position.
            depth (int): The maximum depth of moves to retrieve.

        Returns:
            int: The number of moves found in the principal variation line.
        """
        _assert_condition(depth < MAXDEPTH)
    
        move_obj = self._probe_pv_table(board=board) # instance of MOVE()
        count = 0
        while(move_obj.move != MOVE.NOMOVE and count < depth):
            _assert_condition(count < depth)
            if(move_obj.move_exists(board)): # legal move
                board.make_move(move_obj)
                board.PvArray[count] = move_obj
                count += 1
            else:
                break # we have encountered an illegeal move_obj
            move_obj = self._probe_pv_table(board=board)
            
        while(board.ply > 0):
            board.take_move()
            
        return count

    