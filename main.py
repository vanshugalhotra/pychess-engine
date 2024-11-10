import init
from uci import Uci_Loop
from engine import Engine

if __name__ == "__main__":
    init.initialize()
    eng = Engine()
    print(eng.legal_moves())
    # Uci_Loop()
        
    
    