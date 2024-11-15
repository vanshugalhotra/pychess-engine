import init
from uci import uci_game
from engine import Engine
from fens import WAC1

if __name__ == "__main__":
    init.initialize()
    engine = Engine()
    engine.load_fen(WAC1)
    engine.best_move(depth=4)

    # uci_game()