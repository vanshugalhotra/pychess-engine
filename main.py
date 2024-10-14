import init
from uci import Uci_Loop

PERFTFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 "
WAC1 = "2rr3k/pp3pp1/1nnqbN1p/3pN3/2pP4/2P3Q1/PPB4P/R4RK1 w - -"
WAC2 = "r1b1k2r/ppppnppp/2n2q2/2b5/3NP3/2P1B3/PP3PPP/RN1QKB1R w KQkq - 0 1"
ENDGAME = "6k1/5p2/6p1/8/7p/8/6PP/6K1 b - - 0 0"

if __name__ == "__main__":
    init.AllInit()

    Uci_Loop()
        
    
    