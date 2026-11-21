from maze_workflow import maze_workflow
from typing import Any
import random


def maze_visualizer(vs: Any) -> None:

    """ Trying reading the instructions from the algorithm output """

    def read_instructions() -> str:
        try:
            with open("maze.txt", "r") as maze_info:
                maze: str = maze_info.read()
        except FileNotFoundError:
            raise SystemExit(
                "Run - python3 a_maze_ing.py config.txt - to generate maze.txt"
                        )
        except PermissionError:
            raise SystemExit("Get the permission to read maze.txt")
        except OSError as error:
            raise SystemExit(f"Could not read the file: {error}")
        return maze

    maze = read_instructions()

    """ Parsing the output of the algorithm """

    def parsing_instructions(maze: str) -> tuple[str, str, str, str]:
        maze_instructions, start_end_path = maze.split("\n\n")
        start, end, path, null = start_end_path.split("\n")
        return maze_instructions, start, end, path

    maze_instructions, start, end, path = parsing_instructions(maze)

    """ Finding the dimensions of the maze """

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

    x_maze: int = find_x(maze_instructions)
    y_maze: int = find_y(maze_instructions)

    """ List of the color palettes to change the maze colors """
    if vs.scale % 16 == 0:
        color_0: list[list[int]] = [
            [248, 248, 248, 255],
            [145, 145, 145, 255]
            ]
        color_1: list[list[int]] = [
            [137, 142, 48, 255],
            [208, 201, 186, 255]
            ]
        color_2: list[list[int]] = [
            [175, 103, 61, 255],
            [48, 164, 229, 255]
            ]
        color_3: list[list[int]] = [
            [79, 84, 139, 255],
            [83, 155, 177, 255]
            ]
        color_4: list[list[int]] = [
            [52, 52, 52, 255],
            [255, 255, 255, 255]
            ]
        color: list[list[list[int]]] = [
            color_0,
            color_1,
            color_2,
            color_3,
            color_4
            ]
    else:
        color_0 = [
            [0, 255, 0, 255],
            [255, 0, 0, 255],
            [0, 255, 255, 255],
            [255, 0, 255, 255],
            [255, 255, 0, 255]
            ]
        color_1 = [
            [137, 142, 48, 255],
            [208, 201, 186, 255],
            [255, 255, 255, 255],
            [17, 6, 6, 255],
            [79, 234, 255, 255]
            ]
        color_2 = [
            [175, 103, 61, 255],
            [48, 164, 229, 255],
            [244, 194, 196, 255],
            [211, 209, 208, 255],
            [102, 99, 99, 255]
            ]
        color_3 = [
            [79, 84, 139, 255],
            [83, 155, 177, 255],
            [78, 60, 85, 255],
            [117, 189, 236, 255],
            [156, 189, 165, 255]
            ]
        color_4 = [
            [52, 52, 52, 255],
            [255, 255, 255, 255],
            [141, 141, 141, 255],
            [200, 200, 200, 255],
            [181, 181, 181, 255]
            ]
        color = [
            color_0,
            color_1,
            color_2,
            color_3,
            color_4
            ]
    color_pattern: int = 0

    """ Importing the pictures from .png """

    def import_pictures(vs: Any) -> list[list[list[int]]]:
        pictures: list[str] = [
            "BugCatcher_Pokémon_Yellow.png",
            "Bulbasaur_Pokémon_Yellow.png",
            "Grass_Pokémon_Yellow.png",
            "Pokéball_Pokémon_Yellow.png",
            "Stump_Pokémon_Yellow.png"
        ]
        buffer_pictures: list[list[list[int]]] = []
        for picture in pictures:
            buffer: list[list[int]] = []
            p_a, width, height = vs.m.mlx_png_file_to_image(vs.mlx, picture)
            if p_a is None:
                raise RuntimeError("Could not load PNG")
            else:
                pixels, bpp, size_line, fmt = vs.m.mlx_get_data_addr(p_a)
                x: int = 0
                y: int = 0
                while y < 16:
                    while x < 16:
                        off = (y * size_line) + (x * (bpp // 8))
                        data = bytes(pixels[off:off + 4])
                        buffer.append(list(data))
                        x += 1
                    x = 0
                    y += 1
            buffer_pictures.append(buffer)
        return buffer_pictures

    trainer, pokémon, grass, pokéball, stump = import_pictures(vs)

    """ Uniforming and changing the pictures palette """

    def handling_pixel_color(
        color: list[list[list[int]]],
        color_p: int
                    ) -> None:

        for picture in (trainer, pokémon, grass, pokéball, stump):
            if picture is trainer:
                for px_memory in picture:
                    if px_memory[3] == 0:
                        pass
                    elif px_memory == [248, 248, 248, 255]:
                        px_memory[:] = color[color_p][0]
                    elif px_memory == [168, 168, 168, 255]:
                        px_memory[:] = color[color_p][1]
                    elif px_memory == [0, 0, 0, 255]:
                        pass
            elif picture is pokémon:
                for px_memory in picture:
                    if px_memory[3] == 0:
                        pass
                    elif px_memory == [232, 232, 232, 255]:
                        px_memory[:] = color[color_p][0]
                    elif px_memory == [153, 153, 153, 255]:
                        px_memory[:] = color[color_p][1]
                    elif px_memory == [20, 20, 20, 255]:
                        px_memory[:] = [0, 0, 0, 255]
            elif picture is grass:
                for px_memory in picture:
                    if px_memory[3] == 0:
                        pass
                    elif px_memory == [255, 248, 255, 255]:
                        px_memory[:] = color[color_p][0]
                    elif px_memory == [128, 128, 128, 255]:
                        px_memory[:] = [145, 145, 145, 255]
                    elif px_memory == [0, 0, 0, 255]:
                        pass
                    elif px_memory == [192, 199, 192, 255]:
                        pass
            elif picture is pokéball:
                for px_memory in picture:
                    if px_memory[3] == 0:
                        pass
                    elif px_memory == [232, 232, 232, 255]:
                        px_memory[:] = color[color_p][0]
                    elif px_memory == [153, 153, 153, 255]:
                        px_memory[:] = color[color_p][1]
                    elif px_memory == [20, 20, 20, 255]:
                        px_memory[:] = [0, 0, 0, 255]
            elif picture is stump:
                for px_memory in picture:
                    if px_memory[3] == 0:
                        pass
                    elif px_memory == [255, 248, 255, 255]:
                        px_memory[:] = color[color_p][0]
                    elif px_memory == [128, 128, 128, 255]:
                        px_memory[:] = color[color_p][1]
                    elif px_memory == [0, 0, 0, 255]:
                        pass
                    elif px_memory == [192, 199, 192, 255]:
                        pass

    handling_pixel_color(color, color_pattern)

    """ Creating the image of a scaled grid with cells and walls """

    def visualize_grid(
        m: Any, scale: int,
        color: list[list[list[int]]],
        color_p: int, img: Any
                ) -> None:
        pixels, bpp, size_line, fmt = m.mlx_get_data_addr(img)
        y: int = 0
        x: int = 0
        if vs.scale % 16 == 0:
            while y < (y_maze * scale * 2) + scale:
                if (y // scale) % 2 == 0:
                    while x < (x_maze * scale * 2) + scale:
                        off = (y * size_line) + (x * (bpp // 8))
                        i = (
                            ((y % scale) * 16 // scale) * 16
                            ) + ((x % scale) * 16 // scale)
                        pixels[off:off + 4] = bytes(stump[i])
                        x += 1
                else:
                    while x < (x_maze * scale * 2) + scale:
                        if (x // scale) % 2 == 0:
                            off = (y * size_line) + (x * (bpp // 8))
                            i = (
                                ((y % scale) * 16 // scale) * 16
                                ) + ((x % scale) * 16 // scale)
                            pixels[off:off + 4] = bytes(stump[i])
                        else:
                            off = (y * size_line) + (x * (bpp // 8))
                            i = (
                                ((y % scale) * 16 // scale) * 16
                                ) + ((x % scale) * 16 // scale)
                            pixels[off:off + 4] = bytes(grass[i])
                        x += 1
                y += 1
                x = 0
        else:
            while y < (y_maze * scale * 2) + scale:
                if (y // scale) % 2 == 0:
                    while x < (x_maze * scale * 2) + scale:
                        off = (y * size_line) + (x * (bpp // 8))
                        pixels[off:off + 4] = bytes(color[color_p][0])
                        x += 1
                else:
                    while x < (x_maze * scale * 2) + scale:
                        if (x // scale) % 2 == 0:
                            off = (y * size_line) + (x * (bpp // 8))
                            pixels[off:off + 4] = bytes(color[color_p][0])
                        else:
                            off = (y * size_line) + (x * (bpp // 8))
                            pixels[off:off + 4] = bytes(color[color_p][1])
                        x += 1
                y += 1
                x = 0

    img_lenght: int = (x_maze * vs.scale * 2) + vs.scale  # < vs.x_window
    img_height: int = (y_maze * vs.scale * 2) + vs.scale  # < vs.y_window
    img = vs.m.mlx_new_image(vs.mlx, img_lenght, img_height)
    visualize_grid(vs.m, vs.scale, color, color_pattern, img)

    """ Centering the grid in the window and visualizing it """

    x_position: int = (vs.x_window - ((x_maze * vs.scale * 2) + vs.scale)) // 2
    y_position: int = (vs.y_window - ((y_maze * vs.scale * 2) + vs.scale)) // 2

    vs.m.mlx_put_image_to_window(
        vs.mlx, vs.window,
        img, x_position, y_position
                            )

    """ Making a dict of coordinates (keys) and directions (values) """

    hex_and_dir: dict[str, str] = {
        "0": "NESW", "1": "ESW", "2": "NSW", "3": "SW",
        "4": "NEW", "5": "EW", "6": "NW", "7": "W",
        "8": "NES", "9": "ES", "a": "NS", "b": "S",
        "c": "NE", "d": "E", "e": "N", "f": ""
    }
    coord_and_dir: dict[tuple[int, int], str] = {}
    i: int = 0
    y_coord: int = 0
    x_coord: int = 0
    for hex_dir in maze_instructions:
        if hex_dir == '\n':
            y_coord += 1
            x_coord = 0
            i += 1
        else:
            dir = hex_and_dir.get(maze[i])
            if dir is None:
                raise ValueError("dir unexpectedly None")  # Useless
            coord: tuple[int, int] = (x_coord, y_coord)
            coord_and_dir[(coord)] = dir
            x_coord += 1
            i += 1

    """ From coord_and_dict I create a list of coordinates,
        I shuffle that list, then I open the cell walls in a random order """

    """ -To make the process visualized on the screen-

    draw_state = "spaccando"
    match draw_state:
        case "spaccando_il_maze":
            #disegna
            if finito:
                draw_state = "rivelando il percorso"

        case "rivelando":
            ...
        """

    def open_walls(
        m: Any, x_coord: int, y_coord: int,
        dir: str, scale: int,
        color: list[list[list[int]]],
        color_p: int, img: Any
                ) -> None:
        pixels, bpp, size_line, fmt = m.mlx_get_data_addr(img)
        if not dir:
            if scale % 16 == 0:
                x: int = x_coord * (scale * 2) + (scale * 1)
                y: int = y_coord * (scale * 2) + (scale * 1)
                while y < y_coord * (scale * 2) + (scale * 2):
                    while x < x_coord * (scale * 2) + (scale * 2):
                        off = (y * size_line) + (x * (bpp // 8))
                        i = (
                            ((y % scale) * 16 // scale) * 16
                            ) + ((x % scale) * 16 // scale)
                        pixels[off:off + 4] = bytes(stump[i])
                        x += 1
                    x = x_coord * (scale * 2) + (scale * 1)
                    y += 1
            else:
                x = x_coord * (scale * 2) + (scale * 1)
                y = y_coord * (scale * 2) + (scale * 1)
                while y < y_coord * (scale * 2) + (scale * 2):
                    while x < x_coord * (scale * 2) + (scale * 2):
                        off = (y * size_line) + (x * (bpp // 8))
                        pixels[off:off + 4] = bytes(color[color_p][4])
                        x += 1
                    x = x_coord * (scale * 2) + (scale * 1)
                    y += 1
        for card in dir:
            if scale % 16 == 0:
                if card == "E":
                    x = x_coord * (scale * 2) + (scale * 2)
                    y = y_coord * (scale * 2) + (scale * 1)
                    while y < y_coord * (scale * 2) + (scale * 2):
                        while x < x_coord * (scale * 2) + (scale * 3):
                            off = (y * size_line) + (x * (bpp // 8))
                            i = (
                                ((y % scale) * 16 // scale) * 16
                                ) + ((x % scale) * 16 // scale)
                            pixels[off:off + 4] = bytes(grass[i])
                            x += 1
                        x = x_coord * (scale * 2) + (scale * 2)
                        y += 1
                elif card == "W":
                    x = x_coord * (scale * 2) + (scale * 0)
                    y = y_coord * (scale * 2) + (scale * 1)
                    while y < y_coord * (scale * 2) + (scale * 2):
                        while x < x_coord * (scale * 2) + (scale * 1):
                            off = (y * size_line) + (x * (bpp // 8))
                            i = (
                                ((y % scale) * 16 // scale) * 16
                                ) + ((x % scale) * 16 // scale)
                            pixels[off:off + 4] = bytes(grass[i])
                            x += 1
                        x = x_coord * (scale * 2) + (scale * 0)
                        y += 1
                elif card == "S":
                    x = x_coord * (scale * 2) + (scale * 1)
                    y = y_coord * (scale * 2) + (scale * 2)
                    while y < y_coord * (scale * 2) + (scale * 3):
                        while x < x_coord * (scale * 2) + (scale * 2):
                            off = (y * size_line) + (x * (bpp // 8))
                            i = (
                                ((y % scale) * 16 // scale) * 16
                                ) + ((x % scale) * 16 // scale)
                            pixels[off:off + 4] = bytes(grass[i])
                            x += 1
                        x = x_coord * (scale * 2) + (scale * 1)
                        y += 1
                elif card == "N":
                    x = x_coord * (scale * 2) + (scale * 1)
                    y = y_coord * (scale * 2) + (scale * 0)
                    while y < y_coord * (scale * 2) + (scale * 1):
                        while x < x_coord * (scale * 2) + (scale * 2):
                            off = (y * size_line) + (x * (bpp // 8))
                            i = (
                                ((y % scale) * 16 // scale) * 16
                                ) + ((x % scale) * 16 // scale)
                            pixels[off:off + 4] = bytes(grass[i])
                            x += 1
                        x = x_coord * (scale * 2) + (scale * 1)
                        y += 1
            else:
                if card == "E":
                    x = x_coord * (scale * 2) + (scale * 2)
                    y = y_coord * (scale * 2) + (scale * 1)
                    while y < y_coord * (scale * 2) + (scale * 2):
                        while x < x_coord * (scale * 2) + (scale * 3):
                            off = (y * size_line) + (x * (bpp // 8))
                            pixels[off:off + 4] = bytes(color[color_p][1])
                            x += 1
                        x = x_coord * (scale * 2) + (scale * 2)
                        y += 1
                elif card == "W":
                    x = x_coord * (scale * 2) + (scale * 0)
                    y = y_coord * (scale * 2) + (scale * 1)
                    while y < y_coord * (scale * 2) + (scale * 2):
                        while x < x_coord * (scale * 2) + (scale * 1):
                            off = (y * size_line) + (x * (bpp // 8))
                            pixels[off:off + 4] = bytes(color[color_p][1])
                            x += 1
                        x = x_coord * (scale * 2) + (scale * 0)
                        y += 1
                elif card == "S":
                    x = x_coord * (scale * 2) + (scale * 1)
                    y = y_coord * (scale * 2) + (scale * 2)
                    while y < y_coord * (scale * 2) + (scale * 3):
                        while x < x_coord * (scale * 2) + (scale * 2):
                            off = (y * size_line) + (x * (bpp // 8))
                            pixels[off:off + 4] = bytes(color[color_p][1])
                            x += 1
                        x = x_coord * (scale * 2) + (scale * 1)
                        y += 1
                elif card == "N":
                    x = x_coord * (scale * 2) + (scale * 1)
                    y = y_coord * (scale * 2) + (scale * 0)
                    while y < y_coord * (scale * 2) + (scale * 1):
                        while x < x_coord * (scale * 2) + (scale * 2):
                            off = (y * size_line) + (x * (bpp // 8))
                            pixels[off:off + 4] = bytes(color[color_p][1])
                            x += 1
                        x = x_coord * (scale * 2) + (scale * 1)
                        y += 1
        return

    coords: list[tuple[int, int]] = list(coord_and_dir)
    random.shuffle(coords)
    for coord in coords:
        open_walls(
            vs.m, coord[0], coord[1],
            coord_and_dir[coord], vs.scale,
            color, color_pattern, img
                )
        vs.m.mlx_put_image_to_window(
            vs.mlx, vs.window, img,
            x_position, y_position
                                )

    """ -Coordinates conversion in the img-

        if E(x_coord)
            so x >= x_coord * (scale * 2) + (scale * 2)
            && x < x_coord * (scale * 2) + (scale * 3)
        if E(y_coord)
            so y >= y_coord * (scale * 2) + (scale * 1)
            && y < y_coord * (scale * 2) + (scale * 2)
        if W(x_coord)
            so x >= x_coord * (scale * 2) + (scale * 0)
            && x < x_coord * (scale * 2) + (scale * 1)
        if W(y_coord)
            so y >= y_coord * (scale * 2) + (scale * 1)
            && y < y_coord * (scale * 2) + (scale * 2)
        if S(x_coord)
            so x >= x_coord * (scale * 2) + (scale * 1)
            && x < x_coord * (scale * 2) + (scale * 2)
        if S(y_coord)
            so y >= y_coord * (scale * 2) + (scale * 2)
            && y < y_coord * (scale * 2) + (scale * 3)
        if N(x_coord)
            so x >= x_coord * (scale * 2) + (scale * 1)
            && x < x_coord * (scale * 2) + (scale * 2)
        if N(y_coord)
            so y >= y_coord * (scale * 2) + (scale * 0)
            && y < y_coord * (scale * 2) + (scale * 1)
    """

    """ Visualizing the start and the end inside the maze """

    def visualize_start_end(
        m: Any, x_coord: int, y_coord: int,
        scale: int, img: Any,
        color: list[list[list[int]]], color_p: int, start: bool
                    ) -> None:
        x: int = x_coord * (scale * 2) + (scale * 1)
        y: int = y_coord * (scale * 2) + (scale * 1)
        pixels, bpp, size_line, fmt = m.mlx_get_data_addr(img)
        if scale % 16 == 0:
            while y < y_coord * (scale * 2) + (scale * 2):
                while x < x_coord * (scale * 2) + (scale * 2):
                    off = (y * size_line) + (x * (bpp // 8))
                    i = (
                        ((y % scale) * 16 // scale) * 16
                        ) + ((x % scale) * 16 // scale)
                    if start is True:
                        pixels[off:off + 4] = bytes(trainer[i])
                    else:
                        pixels[off:off + 4] = bytes(pokémon[i])
                    x += 1
                x = x_coord * (scale * 2) + (scale * 1)
                y += 1
        else:
            while y < y_coord * (scale * 2) + (scale * 2):
                while x < x_coord * (scale * 2) + (scale * 2):
                    off = (y * size_line) + (x * (bpp // 8))
                    if start is True:
                        pixels[off:off + 4] = bytes(color[color_p][2])
                    else:
                        pixels[off:off + 4] = bytes(color[color_p][3])
                    x += 1
                x = x_coord * (scale * 2) + (scale * 1)
                y += 1
        return

    x_start, y_start = map(int, start.split(", "))
    x_end, y_end = map(int, end.split(", "))

    visualize_start_end(
        vs.m, x_start, y_start,
        vs.scale, img,
        color, color_pattern, True
                    )
    visualize_start_end(
        vs.m, x_end, y_end,
        vs.scale, img,
        color, color_pattern, False
                    )
    vs.m.mlx_put_image_to_window(
        vs.mlx, vs.window, img,
        x_position, y_position
                            )

    """ Visualizing the path inside the maze """

    def visualize_path(
        m: Any, x_coord: int, y_coord: int,
        path: str, path_visible: bool, scale: int,
        color: list[list[list[int]]], color_p: int, img: Any
                    ) -> None:
        px, bpp, size_line, fmt = m.mlx_get_data_addr(img)
        path_len: int = len(path)
        path_index: int = 0
        if scale % 16 == 0:
            if path_visible is True:
                picture = pokéball
            else:
                picture = grass
            while path_index < path_len:
                if path_index != path_len - 1:
                    if path[path_index] == "E":
                        x: int = x_coord * (scale * 2) + (scale * 2)
                        y: int = y_coord * (scale * 2) + (scale * 1)
                        while y < y_coord * (scale * 2) + (scale * 2):
                            while x < x_coord * (scale * 2) + (scale * 4):
                                off = (y * size_line) + (x * (bpp // 8))
                                i = (
                                    ((y % scale) * 16 // scale) * 16
                                    ) + ((x % scale) * 16 // scale)
                                px[off:off + 4] = bytes(picture[i])
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 2)
                            y += 1
                        x_coord += 1
                    elif path[path_index] == "W":
                        x = x_coord * (scale * 2) + (scale * 0) - scale
                        y = y_coord * (scale * 2) + (scale * 1)
                        while y < y_coord * (scale * 2) + (scale * 2):
                            while x < x_coord * (scale * 2) + (scale * 1):
                                off = (y * size_line) + (x * (bpp // 8))
                                i = (
                                    ((y % scale) * 16 // scale) * 16
                                    ) + ((x % scale) * 16 // scale)
                                px[off:off + 4] = bytes(picture[i])
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 0) - scale
                            y += 1
                        x_coord -= 1
                    elif path[path_index] == "S":
                        x = x_coord * (scale * 2) + (scale * 1)
                        y = y_coord * (scale * 2) + (scale * 2)
                        while y < y_coord * (scale * 2) + (scale * 4):
                            while x < x_coord * (scale * 2) + (scale * 2):
                                off = (y * size_line) + (x * (bpp // 8))
                                i = (
                                    ((y % scale) * 16 // scale) * 16
                                    ) + ((x % scale) * 16 // scale)
                                px[off:off + 4] = bytes(picture[i])
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 1)
                            y += 1
                        y_coord += 1
                    elif path[path_index] == "N":
                        x = x_coord * (scale * 2) + (scale * 1)
                        y = y_coord * (scale * 2) + (scale * 0) - scale
                        while y < y_coord * (scale * 2) + (scale * 1):
                            while x < x_coord * (scale * 2) + (scale * 2):
                                off = (y * size_line) + (x * (bpp // 8))
                                i = (
                                    ((y % scale) * 16 // scale) * 16
                                    ) + ((x % scale) * 16 // scale)
                                px[off:off + 4] = bytes(picture[i])
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 1)
                            y += 1
                        y_coord -= 1
                else:
                    if path[path_index] == "E":
                        x = x_coord * (scale * 2) + (scale * 2)
                        y = y_coord * (scale * 2) + (scale * 1)
                        while y < y_coord * (scale * 2) + (scale * 2):
                            while x < x_coord * (scale * 2) + (scale * 3):
                                off = (y * size_line) + (x * (bpp // 8))
                                i = (
                                    ((y % scale) * 16 // scale) * 16
                                    ) + ((x % scale) * 16 // scale)
                                px[off:off + 4] = bytes(picture[i])
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 2)
                            y += 1
                    elif path[path_index] == "W":
                        x = x_coord * (scale * 2) + (scale * 0)
                        y = y_coord * (scale * 2) + (scale * 1)
                        while y < y_coord * (scale * 2) + (scale * 2):
                            while x < x_coord * (scale * 2) + (scale * 1):
                                off = (y * size_line) + (x * (bpp // 8))
                                i = (
                                    ((y % scale) * 16 // scale) * 16
                                    ) + ((x % scale) * 16 // scale)
                                px[off:off + 4] = bytes(picture[i])
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 0)
                            y += 1
                    elif path[path_index] == "S":
                        x = x_coord * (scale * 2) + (scale * 1)
                        y = y_coord * (scale * 2) + (scale * 2)
                        while y < y_coord * (scale * 2) + (scale * 3):
                            while x < x_coord * (scale * 2) + (scale * 2):
                                off = (y * size_line) + (x * (bpp // 8))
                                i = (
                                    ((y % scale) * 16 // scale) * 16
                                    ) + ((x % scale) * 16 // scale)
                                px[off:off + 4] = bytes(picture[i])
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 1)
                            y += 1
                    elif path[path_index] == "N":
                        x = x_coord * (scale * 2) + (scale * 1)
                        y = y_coord * (scale * 2) + (scale * 0)
                        while y < y_coord * (scale * 2) + (scale * 1):
                            while x < x_coord * (scale * 2) + (scale * 2):
                                off = (y * size_line) + (x * (bpp // 8))
                                i = (
                                    ((y % scale) * 16 // scale) * 16
                                    ) + ((x % scale) * 16 // scale)
                                px[off:off + 4] = bytes(picture[i])
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 1)
                            y += 1
                path_index += 1
        else:
            if path_visible is True:
                color_i: int = 4
            else:
                color_i = 1
            while path_index < path_len:
                if path_index != path_len - 1:
                    if path[path_index] == "E":
                        x = x_coord * (scale * 2) + (scale * 2)
                        y = y_coord * (scale * 2) + (scale * 1)
                        while y < y_coord * (scale * 2) + (scale * 2):
                            while x < x_coord * (scale * 2) + (scale * 4):
                                off = (y * size_line) + (x * (bpp // 8))
                                px[off:off + 4] = bytes(
                                    color[color_p][color_i]
                                        )
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 2)
                            y += 1
                        x_coord += 1
                    elif path[path_index] == "W":
                        x = x_coord * (scale * 2) + (scale * 0) - scale
                        y = y_coord * (scale * 2) + (scale * 1)
                        while y < y_coord * (scale * 2) + (scale * 2):
                            while x < x_coord * (scale * 2) + (scale * 1):
                                off = (y * size_line) + (x * (bpp // 8))
                                px[off:off + 4] = bytes(
                                    color[color_p][color_i]
                                        )
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 0) - scale
                            y += 1
                        x_coord -= 1
                    elif path[path_index] == "S":
                        x = x_coord * (scale * 2) + (scale * 1)
                        y = y_coord * (scale * 2) + (scale * 2)
                        while y < y_coord * (scale * 2) + (scale * 4):
                            while x < x_coord * (scale * 2) + (scale * 2):
                                off = (y * size_line) + (x * (bpp // 8))
                                px[off:off + 4] = bytes(
                                    color[color_p][color_i]
                                        )
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 1)
                            y += 1
                        y_coord += 1
                    elif path[path_index] == "N":
                        x = x_coord * (scale * 2) + (scale * 1)
                        y = y_coord * (scale * 2) + (scale * 0) - scale
                        while y < y_coord * (scale * 2) + (scale * 1):
                            while x < x_coord * (scale * 2) + (scale * 2):
                                off = (y * size_line) + (x * (bpp // 8))
                                px[off:off + 4] = bytes(
                                    color[color_p][color_i]
                                        )
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 1)
                            y += 1
                        y_coord -= 1
                else:
                    if path[path_index] == "E":
                        x = x_coord * (scale * 2) + (scale * 2)
                        y = y_coord * (scale * 2) + (scale * 1)
                        while y < y_coord * (scale * 2) + (scale * 2):
                            while x < x_coord * (scale * 2) + (scale * 3):
                                off = (y * size_line) + (x * (bpp // 8))
                                px[off:off + 4] = bytes(
                                    color[color_p][color_i]
                                        )
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 2)
                            y += 1
                    elif path[path_index] == "W":
                        x = x_coord * (scale * 2) + (scale * 0)
                        y = y_coord * (scale * 2) + (scale * 1)
                        while y < y_coord * (scale * 2) + (scale * 2):
                            while x < x_coord * (scale * 2) + (scale * 1):
                                off = (y * size_line) + (x * (bpp // 8))
                                px[off:off + 4] = bytes(
                                    color[color_p][color_i]
                                        )
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 0)
                            y += 1
                    elif path[path_index] == "S":
                        x = x_coord * (scale * 2) + (scale * 1)
                        y = y_coord * (scale * 2) + (scale * 2)
                        while y < y_coord * (scale * 2) + (scale * 3):
                            while x < x_coord * (scale * 2) + (scale * 2):
                                off = (y * size_line) + (x * (bpp // 8))
                                px[off:off + 4] = bytes(
                                    color[color_p][color_i]
                                        )
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 1)
                            y += 1
                    elif path[path_index] == "N":
                        x = x_coord * (scale * 2) + (scale * 1)
                        y = y_coord * (scale * 2) + (scale * 0)
                        while y < y_coord * (scale * 2) + (scale * 1):
                            while x < x_coord * (scale * 2) + (scale * 2):
                                off = (y * size_line) + (x * (bpp // 8))
                                px[off:off + 4] = bytes(
                                    color[color_p][color_i]
                                        )
                                x += 1
                            x = x_coord * (scale * 2) + (scale * 1)
                            y += 1
                path_index += 1
        return

    path_visible: bool = True
    visualize_path(
        vs.m, x_start, y_start,
        path, path_visible, vs.scale,
        color, color_pattern, img
                )
    vs.m.mlx_put_image_to_window(
        vs.mlx, vs.window, img,
        x_position, y_position
                            )
    path_visible = False

    """ Handling the keyboard inputs """

    def key_press_input(keycode: Any, param: Any) -> None:
        (
            vs, x_position, y_position,
            color, color_p, img_lenght, img_height,
            path_visible, img
        ) = param
        if keycode == 65307:  # Escape input, beware of Windows
            vs.m.mlx_loop_exit(vs.mlx)
        elif keycode == 65289:  # Tab input, beware of Windows
            pixels, bpp, size_line, fmt = vs.m.mlx_get_data_addr(img)
            if vs.scale % 16 == 0:
                handling_pixel_color(color, color_pattern)
                y: int = 0
                x: int = 0
                i: int = 0
                while y < img_height:
                    while x < img_lenght:
                        off = (y * size_line) + (x * (bpp // 8))
                        pixel_color = bytes(pixels[off:off + 4])
                        while (
                            i < len(color[color_p])
                            and bytes(color[color_p][i]) != pixel_color
                                ):
                            if pixel_color[3] == 0:
                                break
                            elif pixel_color == bytes([0, 0, 0, 255]):
                                break
                            elif pixel_color == bytes([192, 199, 192, 255]):
                                break
                            else:
                                i += 1
                        if (
                            i < len(color[color_p])
                            and bytes(color[color_p][i]) == pixel_color
                                ):
                            if color_p < 2:
                                pixels[off:off + 4] = bytes(
                                    color[color_p + 1][i]
                                        )
                            else:
                                pixels[off:off + 4] = bytes(color[0][i])
                        i = 0
                        x += 1
                    x = 0
                    y += 1
            else:
                y = 0
                x = 0
                i = 0
                while y < img_height:
                    while x < img_lenght:
                        off = (y * size_line) + (x * (bpp // 8))
                        pixel_color = bytes(pixels[off:off + 4])
                        while bytes(color[color_p][i]) != pixel_color:
                            i += 1
                        if color_p < 4:
                            pixels[off:off + 4] = bytes(color[color_p + 1][i])
                        else:
                            pixels[off:off + 4] = bytes(color[0][i])
                        i = 0
                        x += 1
                    x = 0
                    y += 1
            if param[4] < 4:
                param[4] += 1
            else:
                param[4] = 0
            vs.m.mlx_put_image_to_window(
                vs.mlx, vs.window, img,
                x_position, y_position
                                    )
        elif keycode == 32:  # Space input, beware of Windows
            if param[7] is True:
                visualize_path(
                    vs.m, x_start, y_start,
                    path, path_visible, vs.scale,
                    color, color_p, img
                            )
                param[7] = False
            else:
                visualize_path(
                    vs.m, x_start, y_start,
                    path, path_visible, vs.scale,
                    color, color_p, img
                            )
                param[7] = True
            vs.m.mlx_put_image_to_window(
                vs.mlx, vs.window,
                img, x_position, y_position
                                    )
        elif keycode == 65288:  # Backspace input, beware of Windows
            vs.m.mlx_destroy_image(vs.mlx, img)
            vs.m.mlx_clear_window(vs.mlx, vs.window)
            vs.seed_count += 1
            maze_workflow(vs.seed_count)
            maze_visualizer(vs)
        return

    params_color = [
        vs, x_position, y_position,
        color, color_pattern,
        img_lenght, img_height,
        path_visible, img
                ]

    vs.m.mlx_hook(vs.window, 2, 1, key_press_input, params_color)

    return
