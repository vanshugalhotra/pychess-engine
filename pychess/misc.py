import sys
import os
from time import time

if os.name == 'nt':  # Check if the system is Windows
    import msvcrt
else:
    import select

def GetTimeMs():
    """
    Returns the current time in milliseconds.
    """
    return int(time() * 1000)

def InputWaiting():
    """
    Checks if there's input waiting on stdin without blocking.
    """
    if os.name == 'nt':  # Windows system
        # On Windows, use msvcrt to check if a key has been pressed
        return msvcrt.kbhit()
    else:  # Unix-like system
        # Using select to check if stdin is ready for reading
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def ReadInput(info):
    """
    Reads input from stdin if any, and sets flags in the info object.
    """
    if InputWaiting():
        info.stopped = True
        if os.name == 'nt':  # Windows system
            input_data = ""
            while msvcrt.kbhit():  # Collect all available characters
                input_data += msvcrt.getch().decode()
            input_data = input_data.strip()
        else:  # Unix-like system
            input_data = sys.stdin.read().strip()  # Read the input and strip newline
        
        # Process input
        if len(input_data) > 0:
            if input_data.startswith("quit"):
                info.quit = True
