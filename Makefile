# ==============================================================================
# A-Maze-ing Makefile
# Created by acirino and dasancil for 42 School
# ==============================================================================

PYTHON        := python3
VENV          := .venv
VENV_PYTHON   := $(VENV)/bin/python
VENV_PIP      := $(VENV)/bin/pip
CONFIG_FILE   := config.txt
MAIN_SCRIPT   := a_maze_ing.py
PACKAGE_NAME  := mazegen

.PHONY: all install package run lint lint-strict debug clean fclean re help

# Default target
all: help

# Create virtual environment, install MLX and local package
install: $(VENV)/bin/activate
	@echo "Installing build tools, linters, and MLX..."
	@$(VENV_PIP) install --upgrade pip build flake8 mypy
	@if [ -f mlx-*.whl ]; then \
		echo "Installing local MLX wheel package..."; \
		$(VENV_PIP) install mlx-*.whl; \
	elif [ -f mlx/mlx-*.whl ]; then \
		echo "Installing MLX wheel from mlx/ directory..."; \
		$(VENV_PIP) install mlx/mlx-*.whl; \
	else \
		echo "Local MLX wheel not found. Attempting install via pip..."; \
		$(VENV_PIP) install mlx || echo "Warning: Could not fetch MLX from PyPI. Ensure mlx-*.whl is placed in root or mlx/"; \
	fi
	@echo "Installing local mazegen package..."
	@$(VENV_PIP) install -e .

$(VENV)/bin/activate:
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV)

# Build the pip-installable package and copy .whl and .tar.gz directly to repository root
package: install
	@echo "Building reusable $(PACKAGE_NAME) package..."
	@$(VENV_PYTHON) -m build
	@cp dist/$(PACKAGE_NAME)-* .
	@echo "Package (.whl and .tar.gz) built and copied directly to repository root."

# Run the main program using virtual environment
run:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Running 'make install' first..."; \
		$(MAKE) install; \
	fi
	@$(VENV_PYTHON) $(MAIN_SCRIPT) $(CONFIG_FILE)

# Code quality checks (flake8 and mypy)
lint:
	@echo "Running flake8 code style checks..."
	@$(VENV_PYTHON) -m flake8 mazegen/ $(MAIN_SCRIPT) mlx_visualizer.py
	@echo "Running mypy static type analysis..."
	@$(VENV_PYTHON) -m mypy mazegen/ $(MAIN_SCRIPT)

# Strict type checking mode
lint-strict:
	@echo "Running strict mypy static type checking..."
	@$(VENV_PYTHON) -m mypy --strict mazegen/ $(MAIN_SCRIPT)

# Run main program in pdb debug mode
debug:
	@$(VENV_PYTHON) -m pdb $(MAIN_SCRIPT) $(CONFIG_FILE)

# Clean build artifacts, pycache, and temporary output files
clean:
	@echo "Cleaning cache files and build outputs..."
	@rm -rf build/ dist/ *.egg-info .mypy_cache .pytest_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -f maze.txt

# Full clean including virtual environment and root wheel/tarball packages
fclean: clean
	@echo "Performing full cleanup..."
	@rm -rf $(VENV)
	@rm -f $(PACKAGE_NAME)-*.whl $(PACKAGE_NAME)-*.tar.gz

# Rebuild virtualenv and package from scratch
re: fclean install package

# Display help information
help:
	@echo "A-Maze-ing Makefile Targets:"
	@echo "  make install     - Create .venv, install MLX, dependencies and mazegen package"
	@echo "  make package     - Build package and place .whl / .tar.gz at repository root"
	@echo "  make run         - Execute a_maze_ing.py with config.txt"
	@echo "  make lint        - Run flake8 and mypy static checks"
	@echo "  make lint-strict - Run mypy with --strict flag"
	@echo "  make debug       - Run main script under pdb debugger"
	@echo "  make clean       - Remove temporary build files, caches, and maze.txt"
	@echo "  make fclean      - Remove .venv, root wheel/tarball packages, and build artifacts"
	@echo "  make re          - Full clean and rebuild"
