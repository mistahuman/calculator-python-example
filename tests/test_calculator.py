"""Tests for calculator module."""

import pytest

from calculator.calculator import add, calculate_average, divide, multiply


class TestCalculator:
    """Test calculator functions."""

    def test_add(self):
        """Test addition."""
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0.5, 0.5) == 1.0

    def test_divide(self):
        """Test division."""
        assert divide(10, 2) == 5
        assert divide(7, 2) == 3.5
        assert divide(-10, 2) == -5

    def test_divide_by_zero(self):
        """Test division by zero raises error."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_multiply(self):
        """Test multiplication."""
        assert multiply(3, 4) == 12
        assert multiply(-2, 3) == -6
        assert multiply(0, 100) == 0

    @pytest.mark.parametrize(
        "numbers,expected",
        [
            ([1, 2, 3], 2.0),
            ([10, 20, 30], 20.0),
            ([5], 5.0),
            ([-1, 0, 1], 0.0),
        ],
    )
    def test_calculate_average(self, numbers, expected):
        """Test average calculation with parametrized inputs."""
        assert calculate_average(numbers) == expected

    def test_calculate_average_empty(self):
        """Test average of empty list raises error."""
        with pytest.raises(ValueError, match="empty list"):
            calculate_average([])


class TestCalculatorIntegration:
    """Integration tests."""

    @pytest.mark.slow
    def test_complex_calculation(self):
        """Test complex calculation workflow."""
        # Simulate complex calculation
        result1 = add(10, 20)
        result2 = multiply(result1, 2)
        final = divide(result2, 3)
        assert final == 20.0
