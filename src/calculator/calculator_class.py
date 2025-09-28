#!/usr/bin/env python3
"""Calculator module with class-based approach.

This module provides a Calculator class with history tracking,
configurable precision, and operation chaining capabilities.

Classes:
    Calculator: Main calculator class with history tracking

Author: Marco Lanconelli
Email: m.lanconelli@example.com
License: MIT
"""

import logging
from typing import List, Optional


class Calculator:
    """Calculator class with history tracking and operation chaining.

    This class provides basic arithmetic operations with additional features:
    - Operation history tracking
    - Configurable precision for results
    - Operation chaining using the last result
    - Logging support

    Attributes:
        precision: Number of decimal places for rounding
        history: List of operation strings
        last_result: The result of the last operation
        logger: Logger instance for debugging

    Examples:
        >>> calc = Calculator(precision=2)
        >>> calc.add(10, 20)
        30.0
        >>> calc.chain_operation("mul", 2)
        60.0
    """

    def __init__(self, precision: int = 2) -> None:
        """Initialize calculator with optional precision.

        Args:
            precision: Number of decimal places for rounding (default: 2)
        """
        self.precision = precision
        self.history: List[str] = []
        self.last_result: Optional[float] = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def add(self, a: float, b: float) -> float:
        """Add two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b, rounded to specified precision
        """
        result = round(a + b, self.precision)
        self._log_operation(f"{a} + {b} = {result}")
        return result

    def divide(self, a: float, b: float) -> float:
        """Divide two numbers.

        Args:
            a: Dividend
            b: Divisor

        Returns:
            Result of a divided by b, rounded to specified precision

        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            self._log_operation(f"{a} / {b} = ERROR", error=True)
            raise ValueError("Cannot divide by zero")
        result = round(a / b, self.precision)
        self._log_operation(f"{a} / {b} = {result}")
        return result

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Product of a and b, rounded to specified precision
        """
        result = round(a * b, self.precision)
        self._log_operation(f"{a} * {b} = {result}")
        return result

    def calculate_average(self, numbers: List[float]) -> float:
        """Calculate average of a list of numbers.

        Args:
            numbers: List of numbers to average

        Returns:
            Average value, rounded to specified precision

        Raises:
            ValueError: If the list is empty
        """
        if not numbers:
            raise ValueError("Cannot calculate average of empty list")
        result = round(sum(numbers) / len(numbers), self.precision)
        self._log_operation(f"avg({numbers}) = {result}")
        return result

    def _log_operation(self, operation: str, error: bool = False) -> None:
        """Log operation to history.

        Private method to track operations in history and update last_result.

        Args:
            operation: String representation of the operation
            error: Whether this operation resulted in an error
        """
        self.history.append(operation)
        if not error:
            self.last_result = float(operation.split("=")[-1].strip())
        self.logger.debug(f"Operation: {operation}")

    def get_history(self) -> List[str]:
        """Get calculation history.

        Returns:
            List of all operations performed
        """
        return self.history

    def clear_history(self) -> None:
        """Clear calculation history and reset last result."""
        self.history = []
        self.last_result = None
        self.logger.info("History cleared")

    def chain_operation(self, op: str, value: float) -> float:
        """Chain operation using last result.

        Performs an operation using the last result as the first operand.

        Args:
            op: Operation name ('add', 'mul', 'div')
            value: Second operand for the operation

        Returns:
            Result of the chained operation

        Raises:
            ValueError: If no previous result exists or unknown operation

        Examples:
            >>> calc = Calculator()
            >>> calc.add(10, 5)  # Result: 15
            15.0
            >>> calc.chain_operation("mul", 2)  # 15 * 2
            30.0
        """
        if self.last_result is None:
            raise ValueError("No previous result to chain")

        operations = {
            "add": lambda x, y: self.add(x, y),
            "mul": lambda x, y: self.multiply(x, y),
            "div": lambda x, y: self.divide(x, y),
        }

        if op not in operations:
            raise ValueError(f"Unknown operation: {op}")

        return operations[op](self.last_result, value)
