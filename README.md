# My Project

A simple calculator library with processing capabilities.

## Features

- Basic arithmetic operations (add, divide, multiply)
- Average calculation
- Operation history tracking
- Configurable precision
- Chain operations support

## Installation

### For development

```bash
pip install -e .[dev]
```

### For production

```bash
pip install -e .
```

## Usage

### Functional Interface

```python
from calculator.calculator import add, multiply, divide

result = add(10, 20)  # 30
result = multiply(5, 6)  # 30
result = divide(10, 2)  # 5.0
```

### Class-Based Interface

```python
from calculator.calculator_class import Calculator

# Create calculator with 2 decimal precision
calc = Calculator(precision=2)

# Basic operations
result = calc.add(10, 20)  # 30.0
result = calc.multiply(5, 6)  # 30.0

# Chain operations
calc.add(10, 5)  # 15
result = calc.chain_operation("mul", 2)  # 30

# View history
print(calc.get_history())
```

## Development

### Running Tests

```bash
make test
```

### Code Formatting

```bash
make format
```

### Linting

```bash
make lint
```

### Type Checking

```bash
make type-check
```

### Generate Documentation

```bash
make docs
```

### Full Check

```bash
make all
```

## Project Structure

```
.
├── Makefile            # Build automation
├── README.md           # This file
├── pyproject.toml      # Project configuration
├── src/
│   └── calculator/     # Main package
│       ├── __init__.py
│       ├── calculator.py       # Functional 
│       └── calculator_class.py # Class-based 
├── tests/              # Test suite
│   ├── test_calculator.py
│   └── test_calculator_class.py
└── docs/               # Documentation
    └── source/
        ├── conf.py     # Sphinx configuration
        └── index.rst   # Documentation index
```

## License

MIT
