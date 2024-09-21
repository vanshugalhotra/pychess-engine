from constants import COLORS

PceChar = ".PNBRQKpnbrqk"
SideChar = "wb-"
RankChar = "12345678"
FileChar = "abcdefgh"

PieceBig = [False, False, True, True, True,True, True, False,True, True, True, True, True]
PieceMaj = [False, False, False, False, True, True, True, False, False, False,True, True, True]
PieceMin = [False, False, True, True, False, False, False, False, True, True,False, False, False]
PieceVal = [0, 100, 325,325,  550, 1000, 50000, 100, 325, 325, 550, 1000, 50000]
PieceCol = [COLORS.BOTH.value, COLORS.WHITE.value, COLORS.WHITE.value, COLORS.WHITE.value, COLORS.WHITE.value, COLORS.WHITE.value, COLORS.WHITE.value, COLORS.BLACK.value, COLORS.BLACK.value, COLORS.BLACK.value, COLORS.BLACK.value, COLORS.BLACK.value, COLORS.BLACK.value]


