from pychess_engine.constants import MAXDEPTH, Colors
from pychess_engine.perft import PerftTest
from pychess_engine.move import MOVELIST
from pychess_engine.engine import Engine
from pychess_engine.fens import START_FEN

NAME = "UstaadJi"
AUTHOR = "Vanshu Galhotra"

test_moves = 0

engine = Engine()

# go depth 6 wtime 180000 btime 100000 binc 1000 winc 1000 movetime 1000 movestogo 40
def ParseGo(line):
    global engine
    depth = MAXDEPTH
    movestogo = 30
    movetime = None
    time = None
    inc = 0
    
    tokens = line.split(" ")
    i = 1 # skip the go keyword
    while i < len(tokens):
        token = tokens[i]
        if(token == "binc"):
            inc = int(tokens[i+1]) if engine.board.side == Colors.BLACK else inc
            i += 2
            
        elif(token == "winc"):
            inc = int(tokens[i+1]) if engine.board.side == Colors.WHITE else inc
            i += 2
            
        elif(token == "wtime"):
            time = int(tokens[i+1]) if engine.board.side == Colors.WHITE else time 
            i += 2
            
        elif(token == "btime"):
            time = int(tokens[i+1]) if engine.board.side == Colors.BLACK else time 
            i += 2
            
        elif(token == "movestogo"):
            movestogo = int(tokens[i+1])
            i += 2
            
        elif(token == "movetime"):
            movetime = int(tokens[i+1])
            i += 2
            
        elif(token == "depth"):
            depth = int(tokens[i+1])
            i += 2
            
        elif(token == "infinite"):
            i += 1
        
        else:
            i += 1
    
    engine.best_move(depth=depth, movestogo=movestogo, movetime=movetime, increment=inc, time=time)
            
# position fen SOMEFENSTRING
# position startpos
# .... moves e2e4 e7e5 b7b8q
def ParsePosition(lineIn):
    global engine
    lineIn = lineIn[9:] # skipping the "Postion "
    charIndex = lineIn
    
    if(lineIn == "startpos"):
        engine.load_fen(fen=START_FEN)
    else:
        charIndex = lineIn.find("fen")
        if(charIndex < 0): # fen not found
            engine.load_fen(fen=START_FEN)
        else:
            charIndex += 4
            engine.load_fen(lineIn[charIndex:])
            
    # processing the moves
    charIndex = lineIn.find("moves")
    move = 0
    if(charIndex >= 0):
        charIndex += 6 # skipped the "moves"
        moves = lineIn[charIndex:].split(" ")
        for mov in moves:
            engine.make_move(move=mov)
            engine.board.ply = 0
    engine.board.print_board()
            

def uci_game():
    global test_moves
    line = ""
    print(f"id name {NAME}")
    print(f"id author {AUTHOR}")
    print(f"uciok")
        
    while(True):
        print()
        line = input()
        if(not line):
            continue
        if(line[0] == '\n'):
            continue
        
        if(line == "isready"):
            print("readyok")
            continue
        elif(line[:8] == "position"):
            ParsePosition(line)
        elif(line == "ucinewgame"):
            ParsePosition("position startpos\n")
        elif(line[:2] == "go"):
            ParseGo(line)
        elif(line[:4] == "quit"):
            engine.controls.quit = True
            break
        elif(line == "uci"):
            print(f"id name {NAME}")
            print(f"id author UstaadJi")
            print(f"uciok")
        elif(line[:6] == "nonuci"):
            coms = line.split()
            move = 0
            if(len(coms) > 1):
                move = coms[1]
            
            if(move == "perft" and len(coms) > 2):
                PerftTest(int(coms[2]), engine.board)
            elif(move == "movelist"):
                mlist = MOVELIST()
                mlist.generate_all_moves(board=engine.board)
                mlist.print_move_list()
            
            elif(move != "take" and move):
                engine.make_move(move=move)
                test_moves += 1
                engine.board.print_board()

            elif(move == "take"):
                if(test_moves):
                    engine.board.take_move()
                    engine.board.print_board()
                    test_moves -= 1
                
        if(engine.controls.quit):
            break

