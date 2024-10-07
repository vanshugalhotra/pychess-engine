import traceback
import sys

DEBUG = False

def assert_condition(condition, message="Assertion failed"):
    if(not DEBUG):
        return True
    if not condition:
        # Get current stack frame
        frame = traceback.extract_stack()[-2]
        
        # Custom message to mimic C-style debugging info
        print(f"{message} ->", end=" ")
        print(f"File: {frame.filename}", end=" ")
        print(f"Line: {frame.lineno}", end=" ")
        print(f"Function: {frame.name}", end=" ")
        sys.exit(1)  # Exit like in the C macro
