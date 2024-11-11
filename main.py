import init
from uci import Uci_Loop
from engine import Engine
from fens import BISHOPS

if __name__ == "__main__":
    init.initialize()
    eng = Engine()
    
    Uci_Loop()
        
    
     