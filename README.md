# A-Maze-ing

*This project has been created as part of the 42 curriculum by acirino, dasancil.*

## Description

**A-Maze-ing** is a modular Python 3.10+ application and reusable library designed to generate, analyze, visualize, and export 2D labyrinths. Built in strict accordance with 42 school software engineering standards, the project features robust error handling, full static type annotations passing `mypy --strict`, compliance with `flake8`, and an event-driven graphical user interface powered by MiniLibX (MLX).

The core engine supports two distinct generation modes governed by the configuration file:
- **Perfect Maze Mode (`PERFECT=True`)**: Generates a classic spanning-tree maze containing exactly one unique topological path between any two points, with zero loops.
- **Playable Board Mode (`PERFECT=False`, default)**: Generates a braided game board with multiple independent loops, reachable corridors, open corners and center, and minimized dead-ends to ensure smooth navigation.

In both modes, the generator integrates a central **"42" pattern** carved by fully closed cells, provided the grid dimensions permit it. The resulting maze structure and its shortest path solution are saved using a standardized hexadecimal wall representation.

---

## Configuration File Specifications

The generator reads a plain-text configuration file containing `KEY=VALUE` pairs. Lines starting with `#` are treated as comments and ignored.

### Key-Value Reference

| Key | Type | Mandatory | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `WIDTH` | Positive `int` | Yes | Total width of the maze in cells | `WIDTH=21` |
| `HEIGHT` | Positive `int` | Yes | Total height of the maze in cells | `HEIGHT=21` |
| `ENTRY` | Tuple `(x,y)` | Yes | Coordinates of the entrance cell | `ENTRY=0,0` |
| `EXIT` | Tuple `(x,y)` | Yes | Coordinates of the exit cell | `EXIT=20,20` |
| `OUTPUT_FILE` | `str` | Yes | Path to save the hexadecimal output | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `bool` | Yes | `True` for single-path, `False` for playable loops | `PERFECT=True` |
| `SEED` | `int` | No | Random seed for deterministic generation | `SEED=42` |
| `ALGORITHM` | `str` | No | Carving algorithm (`backtracker` or `kruskal`) | `ALGORITHM=kruskal` |

### Sample `config.txt`

```ini
# A-Maze-ing Configuration File
WIDTH=21
HEIGHT=21
ENTRY=0,0
EXIT=20,20
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
ALGORITHM=kruskal
```

---

## Output File Format

The output file encodes wall states row-by-row using single hexadecimal digits (`0`–`f`). Each bit of the 4-bit integer represents a closed wall at a cardinal direction:

- **Bit 0 (LSB - 1)**: North wall closed
- **Bit 1 (2)**: East wall closed
- **Bit 2 (4)**: South wall closed
- **Bit 3 (MSB - 8)**: West wall closed

A bit value of `1` signifies a closed wall, while `0` signifies an open passage. Following the grid encoding and a blank line, the file outputs:
1. Entry coordinates `x,y`
2. Exit coordinates `x,y`
3. Shortest path sequence using cardinal directions (`N`, `E`, `S`, `W`)

---

## Maze Generation Algorithms & Technical Choices

The project implements two complementary graph carving algorithms, each tailored to specific maze characteristics:

### 1. Recursive Backtracker (`backtracker`)
- **Mechanism**: A depth-first search algorithm using randomized neighbor selection and an explicit call stack. It carves paths deeply into the grid until it reaches a dead-end, then backtracks to unvisited cells.
- **Why Chosen**: Produces aesthetically pleasing mazes with long, winding corridors and high river factors, making it ideal for standard single-path puzzles.

### 2. Randomized Kruskal's Algorithm (`kruskal`)
- **Mechanism**: Treats grid cells as disjoint sets and wall candidate pairs as edges. Edges are shuffled randomly and processed; if adjacent cells belong to distinct sets, the wall is removed and the sets are merged.
- **Optimization (Jamis Buck Dual-Map Architecture)**: To avoid scanning the entire grid on every wall merge, the implementation uses two synchronized lookup maps: `set_for_cell[cell] -> int` and `cells_in_set[set_id] -> list[Cell]`. When merging, only elements in the smaller set are updated, rendering carving operations nearly instantaneous.
- **Why Chosen**: Guarantees a uniform minimum spanning tree distribution and naturally integrates with the "42" mask by pre-filtering masked neighbor pairs prior to shuffling.

### Mask "42" Handling
Cells forming the "42" logo are flagged at initialization and excluded from neighbor lists. Carving algorithms treat masked cells as permanent obstacles, ensuring the logo remains fully enclosed and untouched.

---

## Reusable Package Architecture (`mazegen`)

The core generation engine is isolated in a standalone, pip-installable Python package named `mazegen`. It contains no GUI or CLI dependencies, preserving strict separation of concerns.

As required by Chapter VI of the 42 subject, the compiled wheel/tarball distribution (`mazegen-1.0.0-py3-none-any.whl` or `mazegen-1.0.0.tar.gz`) is copied directly to the **root of the Git repository** upon building, making it immediately available for standalone installation.

### Installation & Build

Build and copy the wheel distribution directly to the repository root:

```bash
# Option A: Manual build and placement at root
python3 -m pip install --upgrade build
python3 -m build
cp dist/mazegen-1.0.0-py3-none-any.whl .

# Option B: Automated build via Makefile
make package

# Install directly from the package at root
pip install mazegen-1.0.0-py3-none-any.whl
```

### Library Usage Example

```python
from mazegen import MazeGenerator

# Instantiate the generator
maze = MazeGenerator(
    width=21,
    height=21,
    entry=(0, 0),
    exit=(20, 20),
    perfect=True,
    seed=42,
    algorithm="kruskal"
)

# Access generated grid and solution
grid = maze.grid
shortest_path = maze.solution

# Export hexadecimal representation to file stream
with open("maze.txt", "w") as f:
    maze.output(f)
```

---

## Visual Representation & Interactivity

The project features an interactive graphical display built using MiniLibX (MLX) with Python C-types bindings. The visualizer adheres to a Model-View-Controller (MVC) architecture:
- **Model**: `mazegen.MazeGenerator` state and resolution engine.
- **View**: `mlx_visualizer.py` off-screen double-buffering image renderer.
- **Controller**: `a_maze_ing.py` event handler and state manager.

### Interactive Controls

| Key / Input | Action |
| :--- | :--- |
| **`ESC`** | Quit the visualizer and exit cleanly |
| **`BackSpace`** | Re-generate a new maze (increments seed deterministically) |
| **`Space`** | Toggle visibility of the shortest path solution |
| **`Tab`** | Rotate wall and corridor color palettes |

---

## Instructions & Execution

### Prerequisites
- Python 3.10 or later
- Virtual environment framework (`venv`)
- MiniLibX graphical dependencies (X11 / Cocoa)

### Development Setup & Makefile Rules

The project includes a comprehensive `Makefile` to automate setup, building, execution, linting, and cleanup:

```bash
# Clone the repository
git clone <repository_url>
cd a-maze-ing

# Install dependencies, set up .venv, and install mazegen in editable mode
make install

# Build the reusable mazegen package and copy .whl / .tar.gz to root directory
make package

# Run the main application with config.txt
make run

# Run flake8 and mypy static code analysis
make lint

# Run strict mypy type checking
make lint-strict

# Run main script under pdb debugger
make debug

# Clean build artifacts, pycache, and temporary output
make clean

# Perform full clean including virtual environment and root wheel/tarball packages
make fclean

# Rebuild everything from scratch (fclean + install + package)
make re
```

---

## Team & Project Management

### Member Roles & Contributions
- **`acirino`**: Core maze generation engine (`mazegen`), grid data structures, Kruskal & Backtracker carving algorithms, configuration parser, CLI workflow, type hint compliance (`mypy --strict`), Makefile automation, and overall MVC architecture design.
- **`dasancil`**: MiniLibX graphical visualizer (`mlx_visualizer.py`), off-screen image buffer rendering, color palette transformations, coordinate mapping, and keyboard event hook management.

### Project Evolution & Planning
1. **Phase 1 (Initial Setup)**: Grid representations and basic Recursive Backtracker carving.
2. **Phase 2 (Packaging)**: Isolation of `mazegen` into a pip-installable module with `pyproject.toml` and `LICENSE.md`.
3. **Phase 3 (Visualization & Integration)**: Implementation of MiniLibX GUI and refactoring into an MVC pattern to allow non-destructive state updates upon regeneration.
4. **Phase 4 (Optimization & Refinement)**: Refactoring Kruskal's algorithm to use Jamis Buck's dual lookup maps, eliminating quadratic time grid scans.

### Successes & Lessons Learned
- **What Worked Well**: Clean MVC decoupling allowed independent development of the generator and GUI without code collisions.
- **Improvements**: Incorporating automated unit tests (`pytest`) for edge cases in grid dimensions and configuration validation.

---

## Resources & AI Usage Statement

### Technical References
- **Jamis Buck**, *Mazes for Programmers: Code Your Own Twisty Little Passages* (Pragmatic Bookshelf).
- **Nora de Fitero**, *42 MiniLibX Python Manual*.
- **X11 Protocol Specification** (`X.h`).
- **Python Packaging User Guide**, *Packaging Python Projects*.

### AI Usage Disclosure
In accordance with 42 AI Guidelines (Chapter II), AI assistance was utilized as a collaborative thought partner for:
- Writing PEP 257-compliant docstrings and resolving static type hinting warnings in `mypy`.
- Analyzing algorithm complexity for Kruskal's disjoint set implementation and evaluating dual-map optimization.
- Structuring the MVC refactoring plan between `a_maze_ing.py` and `mlx_visualizer.py`.

All AI-generated suggestions were reviewed, manually tested, and refactored by the team prior to integration.
