from pychess.constants import Ranks, Files
from pychess.globals import FilesBrd, RanksBrd, Sq64ToSq120, Sq120ToSq64, clearMask, setMask
from pychess.helper import FR2SQ

def InitSq120To64AndSq64To120():
    sq = 0
    sq64 = 0
    for rank in range(Ranks.R1, Ranks.R8+1): # from rank 1 -> rank 8
        for file in range(Files.A, Files.H + 1): # from file A -> file H
            sq = FR2SQ(file, rank) # calculating the square for 120 bit representation
            Sq64ToSq120[sq64] = sq  # at 0 i.e A1 -> we put 21 i.e FR2SQ(file, rank) 120 bit representation of A1 is 21
            Sq120ToSq64[sq] = sq64  # now sq has 21, so at sq in 120to64 array we put sq64
            sq64 += 1
    
def InitBitMasks():
    for i in range(0, 64):
        setMask[i] = (1 << i) # it will store in powers of 2^i
        clearMask[i] = ~setMask[i] # it will store its complement,
        # lets say, on index 3, setMask[3] will be (In binary) 000000.....1000
        # clearMask[3] will be (IN binary) 11111111.....0111 

def InitFilesRanksBrd():
    for rank in range(Ranks.R1, Ranks.R8+1):
        for file in range(Files.A, Files.H + 1):
            sq = FR2SQ(file, rank)
            FilesBrd[sq] = file
            RanksBrd[sq] = rank     

def initialize():
    InitSq120To64AndSq64To120()
    InitBitMasks()
    InitFilesRanksBrd()

