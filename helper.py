from random import getrandbits

def RAND_64():
    return getrandbits(64)
        
# file rank to the square number (120 squares representation)
def FR2SQ(f, r):
    return (21 + f) + (r * 10)
      