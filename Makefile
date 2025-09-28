.PHONY: help install install-dev test lint format type-check clean build docs coverage all

PYTHON := python
PIP := $(PYTHON) -m pip
SRC := src/calculator
TESTS := tests

help:
	@echo "Available commands:"
	@echo "  make install      Install production dependencies"
	@echo "  make install-dev  Install all dependencies (including dev)"
	@echo "  make test         Run tests with coverage"
	@echo "  make test-fast    Run tests without coverage"
	@echo "  make lint         Run linter (ruff)"
	@echo "  make format       Format code (black + isort)"
	@echo "  make type-check   Run type checker (mypy)"
	@echo "  make clean        Remove build artifacts"
	@echo "  make docs         Build documentation"
	@echo "  make coverage 	   Run and see coverage tests"
	@echo "  make all          Run format, lint, type-check, and test"

install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e .[dev,docs]
	pre-commit install

test:
	pytest

test-fast:
	pytest --no-cov -v

test-watch:
	pytest-watch --clear --nobeep

lint:
	ruff check $(SRC) $(TESTS)

lint-fix:
	ruff check --fix $(SRC) $(TESTS)

format:
	black $(SRC) $(TESTS)
	isort $(SRC) $(TESTS)

format-check:
	black --check $(SRC) $(TESTS)
	isort --check-only $(SRC) $(TESTS)

type-check:
	mypy $(SRC)

check: format-check lint type-check

clean:
	rm -rf build dist *.egg-info
	rm -rf .coverage htmlcov .pytest_cache
	rm -rf .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete


dev: format lint-fix test-fast

all: format lint type-check test

# Documentazione
docs-init:
	sphinx-quickstart docs
	sphinx-apidoc -o docs/source/api src/ -f

docs:
	sphinx-build -b html docs/source docs/build/html

docs-clean:
	rm -rf docs/build

docs-serve:
	python -m http.server -d docs/build/html 8000

coverage:
	rm -rf .coverage htmlcov
	pytest --cov
	python -m http.server -d htmlcov 8001
