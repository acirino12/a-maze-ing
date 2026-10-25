import sys
from mazegen import MazeGenerator


def config_parserer() -> dict[str, str]:
	config: dict[str, str] = dict()
	try:
		with open(sys.argv[1]) as file:
			for line in file:
				line = line.strip()
				if not line or line.startswith('#'):
					continue
				key, value = line.split('=', 1)
				config[key.strip()] = value.strip()
	except Exception:
		print(f"Error: '{sys.argv[1]}' file is not readable", file=sys.stderr)
		sys.exit(1)
	return config


def main() -> None:
	
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments. Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)

    config = config_parserer()
    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        entry = tuple(map(int, config["ENTRY"].split(",")))
        exit = tuple(map(int, config["EXIT"].split(",")))
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
        with open(output_file, 'w') as outfile:
            maze.output(outfile)
    except Exception as e:
        print("Caught Exception on writing output on file:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
