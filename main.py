import init
from uci import Uci_Loop
from engine import Engine
from fens import WAC1

if __name__ == "__main__":
    init.initialize()
    eng = Engine()
    
    eng.load_fen(fen=WAC1)
    # eng.best_move(depth=5)
    
    Uci_Loop()
        
    
     