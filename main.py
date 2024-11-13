import init
from uci import Uci_Loop
from engine import Engine

if __name__ == "__main__":
    init.initialize()
    eng = Engine()
    eng.best_move()
    
    # Uci_Loop()
        
    
     