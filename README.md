
# pychess_engine - A Python Chess Engine

**pychess_engine** is a lightweight chess engine written in Python. It can evaluate chess positions, calculate best moves, and integrate with various interfaces. It is designed to be simple and extensible, offering the flexibility to implement your own chess logic or use it as part of a larger project.

## Features
- Evaluate positions and calculate best moves
- Supports chess rules and common move generation
- Easy integration with Python applications
- Optimized for speed and simplicity



## Installation

Install `pychess_engine` with pip

```bash
    pip install pychess-engine
```
    
# Documentation


## Engine Class

The `Engine` class provides core functionality for a chess engine, including move generation, board management, evaluation, and search for the best move. It is designed to simulate a chess-playing AI, capable of interacting with a chessboard, evaluating positions, and determining optimal moves.

## Attributes

- **name (str)**: Name of the chess engine.
- **author (str)**: Author of the engine.
- **version (str)**: Version of the engine.
- **elo (int)**: ELO rating that adjusts the search depth.
- **controls (EngineControls)**: Manages search control settings.
- **board (Board)**: Represents the current board state.
- **search (Search)**: Manages search algorithms and move evaluation.

### Move Format Used by the Engine

Engine supports standard **co-ordinate based notation** for representing chess moves.

**Example**

For moving pawn from e2 to e4 use `e2e4`

For moving Knight from g1 to f3: `g1f3` is valid ✅ `Nf3` is invalid ❌


## Methods

## `print_board() -> None`
Prints the current board to the console.


```python
from pychess_engine import Engine
engine = Engine()
engine.print_board()

```

## `load_fen(fen: str) -> bool`
Loads a position from a FEN string.

#### Arguments
- **fen (str)**: FEN string representing the board state.

#### Returns
- **bool**: `True` if the FEN string is parsed successfully, `False` otherwise.


```python
from pychess_engine import Engine
engine = Engine()
WAC1 = "2rr3k/pp3pp1/1nnqbN1p/3pN3/2pP4/2P3Q1/PPB4P/R4RK1 w - -"
engine.load_fen(WAC1)
engine.print_board()

```

## `legal_moves() -> list`
Generates all legal moves from the current board position.

#### Returns
- List of all possible moves in algebraic notation.


```python
from pychess_engine import Engine
engine = Engine()
moves = engine.legal_moves()
print(moves)

# also use load_fen() to load a fen and generate moves for that
WAC1 = "2rr3k/pp3pp1/1nnqbN1p/3pN3/2pP4/2P3Q1/PPB4P/R4RK1 w - -"
engine.load_fen(WAC1)
print(engine.legal_moves())

```

## `reset_board() -> None`
Resets the board to the initial starting position.

```python
from pychess_engine import Engine
engine = Engine()

WAC1 = "2rr3k/pp3pp1/1nnqbN1p/3pN3/2pP4/2P3Q1/PPB4P/R4RK1 w - -"
engine.load_fen(WAC1)

engine.reset_board()
engine.print_board()

```

## `make_move(move: str) -> bool`
Attempts to make a move on the board.

#### Arguments
- **move (str)**: Move in algebraic notation (e.g., "e2e4").

#### Returns
- **bool**: `True` if the move is successfully made, `False` if the move is illegal.

```python
from pychess_engine import Engine
engine = Engine()

islegal = engine.make_move("e2e4")
if(not islegal):
    print("Illegal Move!")
engine.print_board()

```

## `is_move_legal(move: str) -> bool`
Checks if a move is legal on the current board.

#### Arguments
- **move (str)**: Move in algebraic notation (e.g., "e2e4").

#### Returns
- **bool**: `True` if the move is legal, `False` otherwise.

```python
from pychess_engine import Engine
engine = Engine()

islegal = engine.is_move_legal("e2e4")
if(islegal):
    print("Legal Move")
else:
    print("Illegal Move")

```

## `set_elo(elo: int) -> None`
Sets the ELO rating for the engine, influencing search depth.

#### Arguments
- **elo (int)**: New ELO rating for the engine.

```python
from pychess_engine import Engine
engine = Engine()

engine.set_elo(1700)

```

## `get_elo() -> int`
Retrieves the current ELO rating of the engine.

#### Returns
- **int**: The current ELO rating.

```python
from pychess_engine import Engine
engine = Engine()

print(engine.get_elo())

```

## `evaluate() -> int`
Evaluates the current board position.

#### Chess Piece Evaluation Scores

- **Pawn**: 100
- **Knight**: 325
- **Bishop**: 325
- **Rook**: 550
- **Queen**: 1000
- **King**: 50000 (INF)

### What it means
- **Positive** Score for **White** means **Advantage** for White
- **Negative** Score for **Black** means **Advantage** for Black


#### Returns
- **int**: Evaluation score of the position.

```python
from pychess_engine import Engine
engine = Engine()

# can load_fen for evaluating specific positions

print(engine.evaluate())

```

## `best_move(depth=None, movestogo=30, movetime=None, increment=0, time=None, display_calculation=True) -> str`
Determines the best move based on search parameters and constraints.

#### Arguments
- **depth (int, optional)**: Search depth for the engine.
- **movestogo (int, optional)**: Number of moves to manage within the available time. **By default 30**
- **movetime (int, optional)**: Time allocated for this move only.
- **increment (int, optional)**: Additional time (increment) per move.
- **time (int, optional)**: Total time available for the current search phase.
- **display_calculation (bool, optional)**: Whether to display the calculation part.

#### Returns
- **str**: The best move in algebraic notation.

```python
from pychess_engine import Engine
engine = Engine()

# can load a fen, or make a move using load_fen, make_move
# can set the elo also

bestmove = engine.best_move()
bestmove = engine.best_move(depth=5) # searching for depth 5
bestmove = engine.best_move(movetime=5000) # specifying the movetime in ms
bestmove = engine.best_move(movestogo=10, time=90000) # 90 seconds divided among 10 moves so each move will get 9 seconds
bestmove = engine.best_move(movetime=3000, increment=1000) # setting the increment

# play around with these controls to get the best out of the engine

print(bestmove)

```

## `perft_test(depth=3) -> None`
Performs Perft (performance test) to calculate the number of legal positions up to a certain depth.

**Only for testing if Move Generation is Accurate or not**

#### Arguments
- **depth (int, optional)**: Depth for the Perft test. Default is 3.

```python
from pychess_engine import Engine
engine = Engine()

engine.perft_test()

```
## Authors

- [@vanshugalhotra](https://www.github.com/vanshugalhotra)


## Acknowledgements

 - [ChessProgrammingWiki](https://www.chessprogramming.org/)
 - [Dr. S. Sangeetha](https://www.nitt.edu/home/academics/departments/ca/facultymca/sangeetha/)

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/). 

You are free to use, modify, and distribute this software under the terms of the MIT License. See the `LICENSE` file for details.

## Feedback

If you have any feedback, please reach out at galhotravanshu@gmail.com or 205124107@nitt.edu


## GitHub Repo

[https://github.com/vanshugalhotra/pychess_engine](https://github.com/vanshugalhotra/pychess_engine)