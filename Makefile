# ==============================================================================
# A-Maze-ing Makefile
# Created for 42 School Curriculum (acirino & dasancil)
# ==============================================================================

PYTHON        := python3
VENV          := .venv
VENV_PYTHON   := $(VENV)/bin/python
VENV_PIP      := $(VENV)/bin/pip
CONFIG_FILE   := config.txt
MAIN_SCRIPT   := a_maze_ing.py
PACKAGE_NAME  := mazegen

.PHONY: all install package run lint lint-strict debug clean fclean re help

all: help

# 1. Environment creation and dependency installation (handles mlx-2.2.tgz automatically)
install: $(VENV)/bin/activate
	@echo "Upgrading build and linting tools..."
	@$(VENV_PIP) install --upgrade pip setuptools wheel build flake8 mypy
	@echo "Installing MLX graphics library..."
	@if [ -f mlx-*.whl ]; then \
		echo "Installing MLX from local wheel..."; \
		$(VENV_PIP) install mlx-*.whl; \
	elif [ -f mlx-2.2.tgz ] || [ -f mlx-*.tgz ]; then \
		TGZ_FILE=$$(ls mlx-*.tgz | head -n 1); \
		echo "Building MLX from source archive ($$TGZ_FILE)..."; \
		mkdir -p .mlx_build && tar -xzf $$TGZ_FILE -C .mlx_build --strip-components=1; \
		if [ -f .mlx_build/configure.sh ]; then \
			(cd .mlx_build && ./configure.sh && make); \
			WHL=$$(find .mlx_build -name "*.whl" | head -n 1); \
			if [ -n "$$WHL" ]; then \
				$(VENV_PIP) install "$$WHL"; \
			else \
				$(VENV_PIP) install .mlx_build || $(VENV_PIP) install mlx || true; \
			fi; \
		else \
			$(VENV_PIP) install .mlx_build || $(VENV_PIP) install mlx || true; \
		fi; \
		rm -rf .mlx_build; \
	else \
		echo "Attempting MLX installation via PyPI..."; \
		$(VENV_PIP) install mlx || echo "Warning: MLX installation skipped or unavailable."; \
	fi
	@echo "Installing local mazegen package in editable mode..."
	@$(VENV_PIP) install -e .

$(VENV)/bin/activate:
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV)

# 2. Package building required by 42 Subject Chapter VI (copies .whl & .tar.gz to root)
package: install
	@echo "Building reusable $(PACKAGE_NAME) package..."
	@$(VENV_PYTHON) -m build
	@cp dist/$(PACKAGE_NAME)-* .
	@echo "Package files (.whl and .tar.gz) successfully placed at repository root."

# 3. Running the application
run:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Running 'make install' first..."; \
		$(MAKE) install; \
	fi
	@$(VENV_PYTHON) $(MAIN_SCRIPT) $(CONFIG_FILE)

# 4. Mandatory 42 Subject Linter Rules (Chapter III.2)
lint:
	@echo "Running flake8 code style checks..."
	@$(VENV_PYTHON) -m flake8 --exclude=.venv,build,dist,.git .
	@echo "Running mypy static type analysis..."
	@$(VENV_PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude '(\.venv|build|dist|\.mlx_build)'

lint-strict:
	@echo "Running strict mypy static type checking..."
	@$(VENV_PYTHON) -m flake8 --exclude=.venv,build,dist,.git .
	@$(VENV_PYTHON) -m mypy . --strict --ignore-missing-imports --exclude '(\.venv|build|dist|\.mlx_build)'

# 5. Debugging
debug:
	@$(VENV_PYTHON) -m pdb $(MAIN_SCRIPT) $(CONFIG_FILE)

# 6. Cleanup
clean:
	@echo "Cleaning cache files, build artifacts, and output files..."
	@rm -rf build/ dist/ *.egg-info .mypy_cache .pytest_cache .mlx_build
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -f maze.txt

fclean: clean
	@echo "Performing full cleanup..."
	@rm -rf $(VENV)
	@rm -f $(PACKAGE_NAME)-*.whl $(PACKAGE_NAME)-*.tar.gz

re: fclean install package

help:
	@echo "A-Maze-ing Makefile Targets:"
	@echo "  make install     - Create .venv, build/install MLX from mlx-2.2.tgz/wheel, and install mazegen"
	@echo "  make package     - Build mazegen wheel & tarball and copy to repo root"
	@echo "  make run         - Execute a_maze_ing.py with config.txt"
	@echo "  make lint        - Run flake8 and mypy according to 42 Subject Chapter III.2"
	@echo "  make lint-strict - Run mypy with --strict"
	@echo "  make debug       - Run main script under pdb debugger"
	@echo "  make clean       - Clean temporary build outputs and caches"
	@echo "  make fclean      - Remove .venv, root package distributions, and build artifacts"
	@echo "  make re          - Perform fclean, install, and package"
