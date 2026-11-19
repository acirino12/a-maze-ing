"""Design pattern is MVC (Model-View-Controller)"""

from typing import Any
from mlx import Mlx
from maze_workflow import maze_workflow
from maze_visualizer import maze_visualizer


class Visualizer:
    def __init__(
        self, m: Any, mlx: Any,
        x_window: int, y_window: int,
        window: Any, seed_count: int
            ):
        self.m = m
        self.mlx = mlx
        self.x_window = x_window
        self.y_window = y_window
        self.window = window
        self.seed_count = seed_count


def main() -> None:

    """Initializing mlx and the window where the image will be visualized"""

    vs = Visualizer(None, None, 1080, 1080, None, 0)
    vs.m = Mlx()
    vs.mlx = vs.m.mlx_init()
    if vs.mlx is None:
        raise RuntimeError("mlx_init() failed")

    vs.window = vs.m.mlx_new_window(
        vs.mlx, vs.x_window,
        vs.y_window, "A-Maze-Ing"
                                )
    if vs.window is None:
        raise RuntimeError("mlx_new_window() failed")
    vs.m.mlx_clear_window(vs.mlx, vs.window)

    """Generating the maze with algorithm"""

    maze_workflow(vs.seed_count)

    """Visualizing the maze through minilibx"""

    maze_visualizer(vs)

    """Loop, close the window and terminating mlx"""

    vs.m.mlx_loop(vs.mlx)
    vs.m.mlx_destroy_window(vs.mlx, vs.window)
    vs.m.mlx_release(vs.mlx)


if __name__ == "__main__":
    main()
