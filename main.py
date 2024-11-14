import init
from uci import uci_game
from engine import Engine
from fens import WAC1

if __name__ == "__main__":
    init.initialize()
    engine = Engine()
    
    
    uci_game()