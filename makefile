# Finance Book Project Makefile

# Variables
PYTHON := python3
PIP := pip3
PY_FILES := $(shell find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" -not -path "./build/*" -not -path "./dist/*")
REQUIREMENTS := requirements.txt

# Test paths
UNIT_TESTS := tests/unit/
INTEGRATION_TESTS := tests/integration/
FUZZ_TESTS := tests/fuzz/

# Default target
.DEFAULT_GOAL := help

.PHONY: help install format lint test clean run setup check-deps backup
.PHONY: test-unit test-integration test-fuzz test-all

help:
	@echo "Finance Book - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  install          - Install project dependencies"
	@echo "  setup            - Setup development environment"
	@echo "  format           - Format code with isort and black"
	@echo "  lint             - Run code quality checks with pylint"
	@echo "  run              - Run the application"
	@echo ""
	@echo "Testing:"
	@echo "  test-unit        - Run unit tests (database.py & router.py)"
	@echo "  test-integration - Run integration tests"
	@echo "  test-fuzz        - Run fuzz tests"
	@echo "  test-all         - Run all tests"
	@echo ""
	@echo "Utilities:"
	@echo "  check-deps       - Check for missing dependencies"
	@echo "  clean            - Clean temporary files and cache"
	@echo "  backup           - Create project backup"
	@echo "  help             - Show this help message"

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
	@$(PIP) install isort black pylint pytest pytest-cov hypothesis
	@if [ -f requirements-test.txt ]; then \
		$(PIP) install -r requirements-test.txt; \
	fi
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

# Unit Tests - 只测试 database.py 和 router.py
test-unit:
	@echo "[INFO] Running unit tests (database.py & router.py)..."
	@$(PYTHON) -m pytest $(UNIT_TESTS) \
		-v \
		--tb=short \
		--cov=models.database \
		--cov=views.router \
		--cov-report=term-missing \
		--cov-fail-under=80
	@echo "[INFO] Unit tests completed"

# Integration Tests
test-integration:
	@echo "[INFO] Running integration tests..."
	@$(PYTHON) -m pytest $(INTEGRATION_TESTS) \
		-v \
		--tb=short
	@echo "[INFO] Integration tests completed"

# Fuzz Tests - 禁用覆盖率，显示 Hypothesis 统计
test-fuzz:
	@echo "[INFO] Running fuzz tests..."
	@$(PYTHON) -m pytest $(FUZZ_TESTS) \
		-v \
		--tb=short \
		--hypothesis-show-statistics \
		-p no:cov
	@echo "[INFO] Fuzz tests completed"

# Run all tests
test-all: test-unit test-integration test-fuzz
	@echo "[SUCCESS] All tests completed"

# Legacy test command (for backwards compatibility)
test: test-all

check-deps:
	@echo "[INFO] Checking Python dependencies..."
	@$(PYTHON) -c "import tkinter; print('tkinter: OK')" 2>/dev/null || echo "[ERROR] tkinter not available"
	@$(PYTHON) -c "import matplotlib; print('matplotlib: OK')" 2>/dev/null || echo "[WARN] matplotlib not installed"
	@$(PYTHON) -c "import pandas; print('pandas: OK')" 2>/dev/null || echo "[WARN] pandas not installed"
	@$(PYTHON) -c "import openpyxl; print('openpyxl: OK')" 2>/dev/null || echo "[WARN] openpyxl not installed"
	@$(PYTHON) -c "import pytest; print('pytest: OK')" 2>/dev/null || echo "[ERROR] pytest not installed"
	@$(PYTHON) -c "import hypothesis; print('hypothesis: OK')" 2>/dev/null || echo "[WARN] hypothesis not installed"

run: check-deps
	@echo "[INFO] Starting Finance Book application..."
	@$(PYTHON) main.py

clean:
	@echo "[INFO] Cleaning temporary files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@rm -rf build/ dist/ .pytest_cache/ htmlcov/ .hypothesis/ 2>/dev/null || true
	@rm -f test.db *.db 2>/dev/null || true
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
		--exclude='htmlcov' \
		--exclude='.hypothesis' \
		.
	@echo "[SUCCESS] Backup created in backups/ directory"

# Development helpers
dev-install: setup
	@echo "[INFO] Installing development tools..."
	@$(PIP) install pre-commit flake8 mypy ruff
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
		rm -f finance_book.db test.db; \
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
	@echo "  Test files: $(shell find tests -name "test_*.py" | wc -l)"
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

# Coverage report (for detailed analysis)
coverage-report:
	@echo "[INFO] Generating detailed coverage report..."
	@$(PYTHON) -m pytest $(UNIT_TESTS) \
		--cov=models.database \
		--cov=views.router \
		--cov-report=html \
		--cov-report=term
	@echo "[SUCCESS] Coverage report generated in htmlcov/index.html"