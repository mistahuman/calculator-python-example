"""Tests for Calculator class."""

import pytest

from calculator.calculator_class import Calculator


class TestCalculatorClass:
    """Test Calculator class."""

    @pytest.fixture
    def calc(self):
        """Create calculator instance."""
        return Calculator(precision=2)

    def test_init(self):
        """Test calculator initialization."""
        calc = Calculator(precision=3)
        assert calc.precision == 3
        assert calc.history == []
        assert calc.last_result is None

    def test_add(self, calc):
        """Test addition with class."""
        result = calc.add(2, 3)
        assert result == 5
        assert calc.last_result == 5
        assert "2 + 3 = 5" in calc.history

    def test_divide_with_history(self, calc):
        """Test division tracks history."""
        result = calc.divide(10, 2)
        assert result == 5
        assert len(calc.history) == 1

    def test_chain_operations(self, calc):
        """Test chaining operations."""
        calc.add(10, 5)  # 15
        result = calc.chain_operation("mul", 2)  # 30
        assert result == 30
        assert calc.last_result == 30

        result = calc.chain_operation("div", 3)  # 10
        assert result == 10

    def test_chain_without_previous(self, calc):
        """Test chain fails without previous result."""
        with pytest.raises(ValueError, match="No previous result"):
            calc.chain_operation("add", 5)

    def test_clear_history(self, calc):
        """Test clearing history."""
        calc.add(1, 2)
        calc.multiply(3, 4)
        assert len(calc.history) == 2

        calc.clear_history()
        assert len(calc.history) == 0
        assert calc.last_result is None

    def test_precision(self):
        """Test precision setting."""
        calc = Calculator(precision=1)
        result = calc.divide(10, 3)
        assert result == 3.3

        calc2 = Calculator(precision=4)
        result = calc2.divide(10, 3)
        assert result == 3.3333
