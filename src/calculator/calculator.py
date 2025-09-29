#!/usr/bin/env python3
"""Calculator module with basic arithmetic operations.

This module provides functional interfaces for basic arithmetic operations
including addition, division, multiplication, and average calculation.

Functions:
    add: Add two numbers
    divide: Divide two numbers with zero-check
    multiply: Multiply two numbers
    calculate_average: Calculate average of a list of numbers

Author: Marco Lanconelli
Email: m.lanconelli@example.com
License: MIT
"""


def add(a: float, b: float) -> float:
    """Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b

    Examples:
        >>> add(2, 3)
        5
        >>> add(-1, 1)
        0
    """
    return a + b


def divide(a: float, b: float) -> float:
    """Divide two numbers.

    Args:
        a: Dividend
        b: Divisor

    Returns:
        Result of a divided by b

    Raises:
        ValueError: If b is zero

    Examples:
        >>> divide(10, 2)
        5.0
        >>> divide(7, 2)
        3.5
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Product of a and b

    Examples:
        >>> multiply(3, 4)
        12
        >>> multiply(-2, 3)
        -6
    """
    return a * b


def calculate_average(numbers: list[float]) -> float:
    """Calculate average of a list of numbers.

    Args:
        numbers: List of numbers to average

    Returns:
        Average value of the numbers

    Raises:
        ValueError: If the list is empty

    Examples:
        >>> calculate_average([1, 2, 3])
        2.0
        >>> calculate_average([10, 20, 30])
        20.0
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)
