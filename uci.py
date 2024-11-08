from constants import SEARCHINFO, START_FEN, COLORS, MAXDEPTH
from pvtable import InitPvTable
from board import Board
from input_output import parseMove
from misc import GetTimeMs
from search import SearchPosition
from move import MOVE

NAME = "UstaadJi"
AUTHOR = "Vanshu Galhotra"
NOMOVE = 0

test_moves = 0

# go depth 6 wtime 180000 btime 100000 binc 1000 winc 1000 movetime 1000 movestogo 40
def ParseGo(line, info, board: Board):
    depth = -1
    movestogo = 30
    movetime = -1
    time = -1
    inc = 0
    info.timeset = False
    
    tokens = line.split(" ")
    i = 1 # skip the go keyword
    while i < len(tokens):
        token = tokens[i]
        if(token == "binc"):
            inc = int(tokens[i+1]) if board.side == COLORS.BLACK.value else inc
            i += 2
            
        elif(token == "winc"):
            inc = int(tokens[i+1]) if board.side == COLORS.WHITE.value else inc
            i += 2
            
        elif(token == "wtime"):
            time = int(tokens[i+1]) if board.side == COLORS.WHITE.value else time 
            i += 2
            
        elif(token == "btime"):
            time = int(tokens[i+1]) if board.side == COLORS.BLACK.value else time 
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
            
    if(movetime != -1): # if movetime is specified
        time = movetime
        movestogo = 1
    
    info.starttime = GetTimeMs()
    info.depth = depth
    
    if(time != -1): # if time is specified in total , then time is divided into movestogo, like 30 mins and movestogo is 40, so each move get 30 mins / 40
        info.timeset = True
        time /= movestogo
        time -= 50 # just to be on safe side
        info.stoptime = info.starttime + time + inc
        
    if(depth == -1): # if depth is not set
        info.depth = MAXDEPTH         
        
    
    print(f"time:{time:.2f} start:{info.starttime:.2f} stop:{info.stoptime:.2f} depth:{info.depth} timeset:{info.timeset}")
    
    SearchPosition(board, info)
            
# position fen SOMEFENSTRING
# position startpos
# .... moves e2e4 e7e5 b7b8q
def ParsePosition(lineIn, board: Board):
    lineIn = lineIn[9:] # skipping the "Postion "
    charIndex = lineIn
    
    if(lineIn == "startpos"):
        board.parse_fen(START_FEN)
    else:
        charIndex = lineIn.find("fen")
        if(charIndex < 0): # fen not found
            board.parse_fen(START_FEN)
        else:
            charIndex += 4
            board.parse_fen(lineIn[charIndex:])
            
    # processing the moves
    charIndex = lineIn.find("moves")
    move = 0
    if(charIndex >= 0):
        charIndex += 6 # skipped the "moves"
        moves = lineIn[charIndex:].split(" ")
        for mov in moves:
            move = parseMove(mov, board)
            if(move == NOMOVE):
                break
            board.make_move(move)
            board.ply = 0
    board.print_board()
            

def Uci_Loop():
    global test_moves
    line = ""
    print(f"id name {NAME}")
    print(f"id author {AUTHOR}")
    print(f"uciok")
    
    pos = Board()
    info = SEARCHINFO()
    InitPvTable(pos.PvTable)
    
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
            ParsePosition(line, pos)
        elif(line == "ucinewgame"):
            ParsePosition("position startpos\n", pos)
        elif(line[:2] == "go"):
            ParseGo(line, info, pos)
        elif(line[:4] == "quit"):
            info.quit = True
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
            if(move != "take" and move):
                parsed_move = parseMove(move, pos)
                if(parsed_move):
                    pos.make_move(parsed_move)
                    test_moves += 1
                    pos.print_board()
                else:
                    print("Invalid Move!")
            elif(move == "take"):
                if(test_moves):
                    pos.take_move()
                    pos.print_board()
                    test_moves -= 1
                
        if(info.quit):
            break

