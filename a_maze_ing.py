import sys
from mazegen import MazeGenerator


def config_parserer() -> dict[str, str]:
    """
    Parse the configuration file specified in command-line arguments.

    Reads key-value pairs separated by '=' from the file path provided in
    sys.argv[1], stripping whitespace and ignoring empty lines or comments
    starting with '#'.

    Returns:
    dict[str, str]: A dictionary containing the configuration keys and their
    corresponding raw string values.
    """
    config: dict[str, str] = dict()
    try:
        with open(sys.argv[1]) as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    except Exception:
        print(f"Error: '{sys.argv[1]}' file is not readable", file=sys.stderr)
        sys.exit(1)
    return config


def parse_coordinate(coord_str: str) -> tuple[int, int]:
    """
    Parse a 'x,y' string into a tuple of two integers.
    """
    parts = coord_str.split(",")
    if len(parts) != 2:
        raise ValueError(
            f"Invalid coordinate '{coord_str}'.",
            "Expected format: 'x,y'"
            )
    return int(parts[0].strip()), int(parts[1].strip())


def main() -> None:
    """Execute the primary maze generation and export workflow.

    Coordinates the configuration parsing, parameter validation, maze
    generation via MazeGenerator, writes the resulting maze structure
    and solution to the designated output file
    ...and launches the interactive terminal visualization.
    """

    if len(sys.argv) != 2:
        print(
            "Error: Invalid number of arguments.",
            " Usage: python3 a_maze_ing.py config.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    config = config_parserer()
    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        entry = parse_coordinate(config["ENTRY"])
        exit = parse_coordinate(config["EXIT"])
        output_file = config["OUTPUT_FILE"]
        if config["PERFECT"] == "True":
            perfect = True
        elif config["PERFECT"] == "False":
            perfect = False
        else:
            raise ValueError("Incorrect parameter 'PERFECT'")
    except Exception as e:
        print("Error", e, file=sys.stderr)
        sys.exit(1)

    seed = None
    if "SEED" in config:
        try:
            seed = int(config["SEED"])
        except Exception as e:
            print("Error", e, file=sys.stderr)
            sys.exit(1)

    try:
        maze = MazeGenerator(width, height, entry, exit, perfect, seed)
    except ValueError as e:
        print(f"Error initializing maze: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(output_file, "w") as outfile:
            maze.output(outfile)
    except Exception as e:
        print(
            "Caught Exception on writing output on file:",
            e,
            file=sys.stderr
            )
        sys.exit(1)


if __name__ == "__main__":
    main()
