import constants

Sq120ToSq64 = [65] * constants.BRD_SQ_NUM # initially every box is 65 (representing offboard)
Sq64ToSq120 = [120] * 64 # initially every box is 120 doesn't mean anything we can put any value

setMask = [0] * 64
clearMask = [0] * 64

PieceKeys = [[0 for _ in range(120)] for _ in range(13)] # will hold random values for each piece on each square

SideKey = -1 # for holding the side value
CastleKeys = [0] * 16 # holding castle values (0 - 15)