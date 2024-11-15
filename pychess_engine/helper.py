from random import getrandbits
from pychess_engine.misc import GetTimeMs

def RAND_64():
    """
    Generates a random 64-bit integer.

    Returns:
        int: A random 64-bit integer, typically used for hashing or 
             generating unique keys in chess board representations.
    """
    return getrandbits(64)
        
# file rank to the square number (120 squares representation)
def FR2SQ(f, r):
    """
    Converts file and rank values to the 120-square board index.

    Args:
        f (int): The file (column) of the square, 0-based.
        r (int): The rank (row) of the square, 0-based.

    Returns:
        int: The 120-square representation index for the given file and rank.
    """
    return (21 + f) + (r * 10)

def execution_time(function):
    """
    Decorator function to measure and print the execution time of a function.

    Args:
        function (Callable): The function whose execution time is to be measured.

    Returns:
        Callable: A wrapped function that prints its execution time in milliseconds.
    """
    def wrapper(*args, **kwargs):
        starttime = GetTimeMs()
        result = function(*args, **kwargs)   
        endtime = GetTimeMs()
        print(f'\tFunction: {function.__name__} Executed in {endtime - starttime}ms')
        return result
        
    return wrapper