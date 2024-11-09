from random import getrandbits
from misc import GetTimeMs

def RAND_64():
    return getrandbits(64)
        
# file rank to the square number (120 squares representation)
def FR2SQ(f, r):
    return (21 + f) + (r * 10)

def execution_time(function):
    def wrapper(*args, **kwargs):
        starttime = GetTimeMs()
        function(*args, **kwargs)   
        endtime = GetTimeMs()
        print(f'\tFunction: {function.__name__} Executed in {endtime - starttime}ms')
        
    return wrapper