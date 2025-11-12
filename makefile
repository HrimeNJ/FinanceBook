# Finance Book Project Makefile

# Variables
PYTHON := python3
PIP := pip3
PY_FILES := $(shell find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" -not -path "./build/*" -not -path "./dist/*")
REQUIREMENTS := requirements.txt

# Default target
.DEFAULT_GOAL := help

.PHONY: help install format lint test clean run setup check-deps backup

help:
	@echo "Finance Book - Available Commands:"
	@echo "  install     - Install project dependencies"
	@echo "  setup       - Setup development environment"
	@echo "  format      - Format code with isort and black"
	@echo "  lint        - Run code quality checks with pylint"
	@echo "  test        - Run unit tests (when available)"
	@echo "  check-deps  - Check for missing dependencies"
	@echo "  run         - Run the application"
	@echo "  clean       - Clean temporary files and cache"
	@echo "  backup      - Create project backup"
	@echo "  help        - Show this help message"

install:
	@echo "[INFO] Installing project dependencies..."
	@if [ -f $(REQUIREMENTS) ]; then \
        $(PIP) install -r $(REQUIREMENTS); \
    else \
        echo "[WARN] No requirements.txt found, installing common dependencies..."; \
        $(PIP) install matplotlib pandas openpyxl; \
    fi
	@echo "[SUCCESS] Dependencies installed successfully"

setup: install
	@echo "[INFO] Setting up development environment..."
	@$(PIP) install isort black pylint pytest
	@echo "[SUCCESS] Development environment ready"

format:
	@echo "[INFO] Formatting Python code..."
	@echo "  - Running isort (import sorting)..."
	@isort $(PY_FILES) --quiet
	@echo "  - Running black (code formatting)..."
	@black $(PY_FILES) --quiet
	@echo "[SUCCESS] Code formatting completed"

lint:
	@echo "[INFO] Running code quality checks..."
	@pylint --jobs=0 --score=yes $(PY_FILES) || true
	@echo "[INFO] Lint check completed"

test:
	@echo "[INFO] Running unit tests..."
	@if [ -d "tests" ]; then \
        $(PYTHON) -m pytest tests/ -v; \
    else \
        echo "[WARN] No tests directory found"; \
    fi

check-deps:
	@echo "[INFO] Checking Python dependencies..."
	@$(PYTHON) -c "import tkinter; print('tkinter: OK')" 2>/dev/null || echo "[ERROR] tkinter not available"
	@$(PYTHON) -c "import matplotlib; print('matplotlib: OK')" 2>/dev/null || echo "[WARN] matplotlib not installed"
	@$(PYTHON) -c "import pandas; print('pandas: OK')" 2>/dev/null || echo "[WARN] pandas not installed"
	@$(PYTHON) -c "import openpyxl; print('openpyxl: OK')" 2>/dev/null || echo "[WARN] openpyxl not installed"

run: check-deps
	@echo "[INFO] Starting Finance Book application..."
	@$(PYTHON) main.py

clean:
	@echo "[INFO] Cleaning temporary files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@rm -rf build/ dist/ .pytest_cache/ 2>/dev/null || true
	@echo "[SUCCESS] Cleanup completed"

backup:
	@echo "[INFO] Creating project backup..."
	@mkdir -p backups
	@tar -czf backups/finance_book_backup_$(shell date +%Y%m%d_%H%M%S).tar.gz \
        --exclude='.git' \
        --exclude='venv' \
        --exclude='.venv' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='backups' \
        .
	@echo "[SUCCESS] Backup created in backups/ directory"

# Development helpers
dev-install: setup
	@echo "[INFO] Installing development tools..."
	@$(PIP) install pre-commit flake8 mypy
	@echo "[SUCCESS] Development tools installed"

quick-check: format lint
	@echo "[INFO] Quick code quality check completed"

# Database operations
init-db:
	@echo "[INFO] Initializing database..."
	@$(PYTHON) -c "from models.database import DatabaseManager; db = DatabaseManager(); print('Database initialized')"

reset-db:
	@echo "[WARN] This will delete all data. Continue? [y/N]"
	@read answer; if [ "$$answer" = "y" ]; then \
        rm -f finance_book.db; \
        echo "[INFO] Database reset completed"; \
    else \
        echo "[INFO] Database reset cancelled"; \
    fi

# Show project info
info:
	@echo "Finance Book Project Information:"
	@echo "  Python version: $(shell $(PYTHON) --version)"
	@echo "  Project files: $(words $(PY_FILES)) Python files"
	@echo "  Database file: finance_book.db"
	@echo "  Last modified: $(shell stat -c %y main.py 2>/dev/null || stat -f %Sm main.py 2>/dev/null || echo 'Unknown')"

# Quick run without dependency check
quick-run:
	@$(PYTHON) main.py

# Show directory structure
tree:
	@echo "Project Structure:"
	@find . -type f -name "*.py" | head -20 | sed 's|^\./||' | sort
	@echo "..."
	@echo "Total Python files: $(words $(PY_FILES))"