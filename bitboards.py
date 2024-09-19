import constants
import globals

def PrintBitBoard(bb):
    shiftMe = 1
    sq = 0
    sq64 = 0
    print()
    for rank in range(constants.RANK.R8.value, constants.RANK.R1.value - 1, -1): #7-0
        for file in range(constants.FILE.A.value, constants.FILE.H.value+1): #0-7
            sq = constants.FR2SQ(file, rank) # calculating the square for 120 bit
            sq64 = globals.Sq120ToSq64[sq] # converting the square for 64 bit
            if((shiftMe << sq64) & bb):
                print("X", end=" ")
            else:
                print("-", end=" ")
        print()
        
def CountBits(b):
    r = 0
    while(b):
        b = b & b-1
        r += 1
    return r
        
def PopBit(bb):
    # Isolate the least significant bit (LSB)
    lsb = bb & -bb

    # Find the index of the LSB using bit_length
    index = (lsb.bit_length() - 1)

    # Remove the LSB from the bitboard
    bb &= bb - 1

    return index, bb

