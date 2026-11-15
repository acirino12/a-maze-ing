from mlx import Mlx
from maze_workflow import maze_workflow
import random
import time

def visualize_path(m, x_coord, y_coord, path, scale, color, color_index, img):
    pixels, bpp, size_line, fmt = m.mlx_get_data_addr(img)
    path_len: int = len(path)
    path_index: int = 0
    while path_index < path_len:
        if path_index != path_len - 1: # if path_index == 0:
            if path[path_index] == "E":
                x: int = x_coord * (scale * 2) + (scale * 2)
                y: int = y_coord * (scale * 2) + (scale * 1)
                while y < y_coord * (scale * 2) + (scale * 2):
                    while x < x_coord * (scale * 2) + (scale * 4):
                        offset = (y * size_line) + (x * (bpp // 8))
                        pixels[offset:offset + 4] = bytes(color[color_index]) # cyan - path 4
                        x += 1
                    x = x_coord * (scale * 2) + (scale * 2)
                    y += 1
                x_coord += 1
            elif path[path_index] == "W":
                x: int = x_coord * (scale * 2) + (scale * 0) - scale
                y: int = y_coord * (scale * 2) + (scale * 1)
                while y < y_coord * (scale * 2) + (scale * 2):
                    while x < x_coord * (scale * 2) + (scale * 1):
                        offset = (y * size_line) + (x * (bpp // 8))
                        pixels[offset:offset + 4] = bytes(color[color_index]) # cyan - path 4
                        x += 1
                    x = x_coord * (scale * 2) + (scale * 0) - scale
                    y += 1
                x_coord -= 1
            elif path[path_index] == "S":
                x: int = x_coord * (scale * 2) + (scale * 1)
                y: int = y_coord * (scale * 2) + (scale * 2)
                while y < y_coord * (scale * 2) + (scale * 4):
                    while x < x_coord * (scale * 2) + (scale * 2):
                        offset = (y * size_line) + (x * (bpp // 8))
                        pixels[offset:offset + 4] = bytes(color[color_index]) # cyan - path 4
                        x += 1
                    x = x_coord * (scale * 2) + (scale * 1)
                    y += 1
                y_coord += 1
            elif path[path_index] == "N":
                x: int = x_coord * (scale * 2) + (scale * 1)
                y: int = y_coord * (scale * 2) + (scale * 0) - scale
                while y < y_coord * (scale * 2) + (scale * 1):
                    while x < x_coord * (scale * 2) + (scale * 2):
                        offset = (y * size_line) + (x * (bpp // 8))
                        pixels[offset:offset + 4] = bytes(color[color_index]) # cyan - path 4
                        x += 1
                    x = x_coord * (scale * 2) + (scale * 1)
                    y += 1
                y_coord -= 1
        else:
            if path[path_index] == "E":
                x: int = x_coord * (scale * 2) + (scale * 2)
                y: int = y_coord * (scale * 2) + (scale * 1)
                while y < y_coord * (scale * 2) + (scale * 2):
                    while x < x_coord * (scale * 2) + (scale * 3):
                        offset = (y * size_line) + (x * (bpp // 8))
                        pixels[offset:offset + 4] = bytes(color[color_index]) # cyan - path
                        x += 1
                    x = x_coord * (scale * 2) + (scale * 2)
                    y += 1
            elif path[path_index] == "W":
                x: int = x_coord * (scale * 2) + (scale * 0)
                y: int = y_coord * (scale * 2) + (scale * 1)
                while y < y_coord * (scale * 2) + (scale * 2):
                    while x < x_coord * (scale * 2) + (scale * 1):
                        offset = (y * size_line) + (x * (bpp // 8))
                        pixels[offset:offset + 4] = bytes(color[color_index]) # cyan - path
                        x += 1
                    x = x_coord * (scale * 2) + (scale * 0)
                    y += 1
            elif path[path_index] == "S":
                x: int = x_coord * (scale * 2) + (scale * 1)
                y: int = y_coord * (scale * 2) + (scale * 2)
                while y < y_coord * (scale * 2) + (scale * 3):
                    while x < x_coord * (scale * 2) + (scale * 2):
                        offset = (y * size_line) + (x * (bpp // 8))
                        pixels[offset:offset + 4] = bytes(color[color_index]) # cyan - path
                        x += 1
                    x = x_coord * (scale * 2) + (scale * 1)
                    y += 1
            elif path[path_index] == "N":
                x: int = x_coord * (scale * 2) + (scale * 1)
                y: int = y_coord * (scale * 2) + (scale * 0)
                while y < y_coord * (scale * 2) + (scale * 1):
                    while x < x_coord * (scale * 2) + (scale * 2):
                        offset = (y * size_line) + (x * (bpp // 8))
                        pixels[offset:offset + 4] = bytes(color[color_index]) # cyan - path
                        x += 1
                    x = x_coord * (scale * 2) + (scale * 1)
                    y += 1
        path_index += 1
    return

def visualize_start_end (m, x_coord, y_coord, scale, img, color, start):
    x: int = x_coord * (scale * 2) + (scale * 1)
    y: int = y_coord * (scale * 2) + (scale * 1)
    pixels, bpp, size_line, fmt = m.mlx_get_data_addr(img)
    while y < y_coord * (scale * 2) + (scale * 2):
        while x < x_coord * (scale * 2) + (scale * 2):
            offset = (y * size_line) + (x * (bpp // 8))
            if start is True:
                pixels[offset:offset + 4] = bytes(color[2]) # yellow - start
            else:
                pixels[offset:offset + 4] = bytes(color[3]) # magenta - end
            x += 1
        x = x_coord * (scale * 2) + (scale * 1)
        y += 1
    return

def open_walls(m, x_coord, y_coord, dir, scale, color, img):
    pixels, bpp, size_line, fmt = m.mlx_get_data_addr(img)
    for card in dir:
        if card == "E":
            x: int = x_coord * (scale * 2) + (scale * 2)
            y: int = y_coord * (scale * 2) + (scale * 1)
            while y < y_coord * (scale * 2) + (scale * 2):
                while x < x_coord * (scale * 2) + (scale * 3):
                    offset = (y * size_line) + (x * (bpp // 8))
                    pixels[offset:offset + 4] = bytes(color[1]) # blue - openwall
                    x += 1
                x = x_coord * (scale * 2) + (scale * 2)
                y += 1
        elif card == "W":
            x: int = x_coord * (scale * 2) + (scale * 0)
            y: int = y_coord * (scale * 2) + (scale * 1)
            while y < y_coord * (scale * 2) + (scale * 2):
                while x < x_coord * (scale * 2) + (scale * 1):
                    offset = (y * size_line) + (x * (bpp // 8))
                    pixels[offset:offset + 4] = bytes(color[1]) # blue - openwall
                    x += 1
                x = x_coord * (scale * 2) + (scale * 0)
                y += 1
        elif card == "S":
            x: int = x_coord * (scale * 2) + (scale * 1)
            y: int = y_coord * (scale * 2) + (scale * 2)
            while y < y_coord * (scale * 2) + (scale * 3):
                while x < x_coord * (scale * 2) + (scale * 2):
                    offset = (y * size_line) + (x * (bpp // 8))
                    pixels[offset:offset + 4] = bytes(color[1]) # blue - openwall
                    x += 1
                x = x_coord * (scale * 2) + (scale * 1)
                y += 1
        elif card == "N":
            x: int = x_coord * (scale * 2) + (scale * 1)
            y: int = y_coord * (scale * 2) + (scale * 0)
            while y < y_coord * (scale * 2) + (scale * 1):
                while x < x_coord * (scale * 2) + (scale * 2):
                    offset = (y * size_line) + (x * (bpp // 8))
                    pixels[offset:offset + 4] = bytes(color[1]) # blue - openwall
                    x += 1
                x = x_coord * (scale * 2) + (scale * 1)
                y += 1
    return

def find_x(maze_dir: str) -> int:
    x: int = 0
    while maze_dir[x] != '\n':
        x += 1
    return (x)

def find_y(maze_dir: str) -> int:
    x: int = 0
    y: int = 0
    for dir in maze_dir:
        if dir == '\n':
            y += 1
        x += 1
    return (y + 1)

def maze_visualizer(vs) -> None:

    # Trying reading the instructions from the algorithm output
    
    def read_instructions() -> str:
        try:
            with open("maze.txt", "r") as maze_info:
                maze: str = maze_info.read()
        except FileNotFoundError:
            raise SystemExit("Run - python3 a_maze_ing.py config.txt - to generate maze.txt")
        except PermissionError:
            raise SystemExit("Get the permission to read maze.txt")
        except OSError as error:
            raise SystemExit(f"Could not read the file: {error}")
        return maze

    maze = read_instructions()

    # Parsing the output of the algorithm

    def parsing_instructions(maze) -> tuple[str, str, str, str]:
        maze_instructions, start_end_path = maze.split("\n\n")
        start, end, path, null = start_end_path.split("\n") # null is there because there is a trailing \n in maze.txt
        return maze_instructions, start, end, path

    maze_instructions, start, end, path = parsing_instructions(maze)

    """ - Initializing mlx and the window where the image will be visualized (moved to main a-maze-ing.py) -
    m = Mlx()
    mlx = m.mlx_init()
    if mlx is None:
        raise RuntimeError("mlx_init() failed")

    x_window: int = 1080
    y_window: int = 1080

    window = m.mlx_new_window(mlx, x_window, y_window, "A-Maze-Ing")
    if window is None:
        raise RuntimeError("mlx_new_window() failed")
    m.mlx_clear_window(mlx, window)
    """

    # Finding the dimensions of the maze

    x_maze: int = find_x(maze_instructions)
    y_maze: int = find_y(maze_instructions)

    # List of list of colors to change the maze colors

    color: list = [
        [0, 255, 0, 255],
        [255, 0, 0, 255],
        [0, 255, 255, 255],
        [255, 0, 255, 255],
        [255, 255, 0, 255]
    ]

    # Creation of the image of a scaled grid with cells and walls

    def visualize_grid(m, scale, color, img) -> None:
        pixels, bpp, size_line, fmt = m.mlx_get_data_addr(img)
        y: int = 0
        x: int = 0
        while y < (y_maze * scale * 2) + scale:
            if (y // scale) % 2 == 0:
                while x < (x_maze * scale * 2) + scale:
                    offset = (y * size_line) + (x * (bpp // 8))
                    pixels[offset:offset + 4] = bytes(color[0]) # green - wall
                    x += 1
            else:
                while x < (x_maze * scale * 2) + scale:
                    if (x // scale) % 2 == 0:
                        offset = (y * size_line) + (x * (bpp // 8))
                        pixels[offset:offset + 4] = bytes(color[0]) # green - wall
                    else:
                        offset = (y * size_line) + (x * (bpp // 8))
                        pixels[offset:offset + 4] = bytes(color[1]) # blue - cell
                    x += 1
            y += 1
            x = 0

    scale: int = 4
    img_lenght: int = (x_maze * scale * 2) + scale # < vs.x_window
    img_height: int = (y_maze * scale * 2) + scale # < vs.y_window
    img = vs.m.mlx_new_image(vs.mlx, img_lenght, img_height)
    visualize_grid(vs.m, scale, color, img)

    # Center the grid in the window and visualize it

    x_position: int = (vs.x_window - ((x_maze * scale * 2) + scale)) // 2
    y_position: int = (vs.y_window - ((y_maze * scale * 2) + scale)) // 2

    vs.m.mlx_put_image_to_window(vs.mlx, vs.window, img, x_position, y_position)

    # Prendere le coordinate e i muri dal maze.txt

    ## Ottenere dizionario di coordinate e direzioni associate (manca un while)

    hex_and_dir: dict = {
        "0": "NESW", "1": "ESW", "2": "NSW", "3": "SW",
        "4": "NEW", "5": "EW", "6": "NW", "7": "W",
        "8": "NES", "9": "ES", "a": "NS", "b": "S",
        "c": "NE", "d": "E", "e": "N", "f": ""
    }
    coord_and_dir: dict = {}
    i: int = 0
    y_coord: int = 0
    x_coord: int = 0
    for hex_dir in maze_instructions:
        if hex_dir == '\n':
            y_coord += 1
            x_coord = 0
            i += 1
        else:
            dir: str = hex_and_dir.get(maze[i])
            coord: tuple = (x_coord, y_coord)
            coord_and_dir[(coord)] = dir
            x_coord += 1
            i += 1

    ## From coord_and_dict I create a list of coordinates that I shuffle, then I open the cells' walls in a random order

    """ 

    draw_state = "spaccando"
    match draw_state:
        case "spaccando_il_maze":
            #disegna
            if finito:
                draw_state = "rivelando il percorso"
                
        case "rivelando":
            ...
        """

    coords: list = list(coord_and_dir)
    random.shuffle(coords)
    for coord in coords:
        open_walls(vs.m, coord[0], coord[1], coord_and_dir[coord], scale, color, img)
        vs.m.mlx_put_image_to_window(vs.mlx, vs.window, img, x_position, y_position)
        #time.sleep(0.5)

    # Visualize the start and the end of the maze

    x_start, y_start = map(int, start.split(", "))
    x_end, y_end = map(int, end.split(", "))

    visualize_start_end(vs.m, x_start, y_start, scale, img, color, True)
    visualize_start_end(vs.m, x_end, y_end, scale, img, color, False)   
    vs.m.mlx_put_image_to_window(vs.mlx, vs.window, img, x_position, y_position)

    # Visualize the path inside the maze

    # print(path) | DEBUG - controllo del percorso
    visualize_path(vs.m, x_start, y_start, path, scale, color, 4, img)
    vs.m.mlx_put_image_to_window(vs.mlx, vs.window, img, x_position, y_position)
    
        
# se E(x_coord) allora x >= x_coord * (scale * 2) + (scale * 2) && x < x_coord * (scale * 2) + (scale * 3)
# se E(y_coord) allora y >= y_coord * (scale * 2) + (scale * 1) && y < y_coord * (scale * 2) + (scale * 2)
# se W(x_coord) allora x >= x_coord * (scale * 2) + (scale * 0) && x < x_coord * (scale * 2) + (scale * 1)
# se W(y_coord) allora y >= y_coord * (scale * 2) + (scale * 1) && y < y_coord * (scale * 2) + (scale * 2)
# se S(x_coord) allora x >= x_coord * (scale * 2) + (scale * 1) && x < x_coord * (scale * 2) + (scale * 2)
# se S(y_coord) allora y >= y_coord * (scale * 2) + (scale * 2) && y < y_coord * (scale * 2) + (scale * 3)
# se N(x_coord) allora x >= x_coord * (scale * 2) + (scale * 1) && x < x_coord * (scale * 2) + (scale * 2)
# se N(y_coord) allora y >= y_coord * (scale * 2) + (scale * 0) && y < y_coord * (scale * 2) + (scale * 1)

    def key_press_input(keycode, param):
        vs, x_position, y_position, color, color_pattern, img_lenght, img_height, path_visible, img = param
        if keycode == 65307: # Input di Escape su Linux, controllare su Windows
            vs.m.mlx_loop_exit(vs.mlx)
        elif keycode == 65289: # Input di Tab, controllare su Windows
            pixels, bpp, size_line, fmt = vs.m.mlx_get_data_addr(img)
            y: int = 0
            x: int = 0
            i: int = 0
            while y < img_height:
                while x < img_lenght:
                    offset = (y * size_line) + (x * (bpp // 8))
                    pixel_color = bytes(pixels[offset:offset + 4]) # green - wall
                    while bytes(color[i]) != pixel_color:
                        i += 1
                    if i < 4:
                        pixels[offset:offset + 4] = bytes(color[i + 1])
                    else:
                        pixels[offset:offset + 4] = bytes(color[0])
                    i = 0
                    x += 1        
                x = 0
                y += 1
            if param[4] < 4:
                param[4] += 1
            else:
                param[4] = 0            
            vs.m.mlx_put_image_to_window(vs.mlx, vs.window, img, x_position, y_position)
        elif keycode == 32: # Input di Space, controllare su Windows
            if param[7] is True:
                visualize_path(vs.m, x_start, y_start, path, scale, color, ((1 + param[7]) % 5), img)
                param[7] = False
            else:
                visualize_path(vs.m, x_start, y_start, path, scale, color, ((4 + param[7]) % 5), img)
                param[7] = True
            vs.m.mlx_put_image_to_window(vs.mlx, vs.window, img, x_position, y_position)
        elif keycode == 65288: # Input di Backspace, controllare su Windows
            vs.m.mlx_destroy_image(vs.mlx, img)
            vs.m.mlx_clear_window(vs.mlx, vs.window)
            vs.seed_count += 1
            maze_workflow(vs.seed_count)
            maze_visualizer(vs)
        return

    color_pattern: int = 0
    path_visible: bool = True
    params_color = [vs, x_position, y_position, color, color_pattern, img_lenght, img_height, path_visible, img]    

    vs.m.mlx_hook(vs.window, 2, 1, key_press_input, params_color)
    # m.mlx_hook(window, 2, 1, maze_key, None) #Backspace
    """ - Loop, close the window and terminating mlx (moved in a-maze-ing.py) -
    vs.m.mlx_loop(vs.mlx)
    vs.m.mlx_destroy_window(vs.mlx, vs.window)
    vs.m.mlx_release(vs.mlx)
    """

    return
