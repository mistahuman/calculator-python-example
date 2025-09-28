#!/usr/bin/env python3
"""My Project - A simple calculator with processing capabilities.

This package provides both functional and class-based interfaces for
performing basic arithmetic operations with additional features like
history tracking and operation chaining.

Author: Marco Lanconelli
Email: m.lanconelli@example.com
License: MIT
"""

__version__ = "0.1.0"
__project__ = "Calculator"
__author__ = "Marco Lanconelli"
__email__ = "m.lanconelli@example.com"

from calculator.calculator import add, calculate_average, divide, multiply
from calculator.calculator_class import Calculator

# import logging
# logging.basicConfig(
#     level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )


__all__ = [
    "add",
    "divide",
    "multiply",
    "calculate_average",
    "Calculator",
]
