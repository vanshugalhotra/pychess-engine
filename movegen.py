

def AddQuietMove(board, move, list):
    list.moves[list.count].move = move
    list.moves[list.count].score = 0
    list.count += 1
    
def AddCaptureMove(board, move, list):
    list.moves[list.count].move = move
    list.moves[list.count].score = 0
    list.count += 1
    
def AddEnPassantMove(board, move, list):
    list.moves[list.count].move = move
    list.moves[list.count].score = 0
    list.count += 1