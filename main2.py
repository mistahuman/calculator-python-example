#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main entry point for the calculator application.

This module provides a simple CLI interface to demonstrate
the calculator functionality.

Author: Marco Lanconelli
Email: m.lanconelli@example.com
License: MIT
"""

import sys
from calculator.calculator import add, divide, multiply, calculate_average
from calculator.calculator_class import Calculator


def main():
    """Main function to demonstrate calculator usage."""
    print("Calculator Demo")
    print("=" * 40)
    
    # Functional interface demo
    print("\n1. Functional Interface Demo:")
    print(f"  10 + 20 = {add(10, 20)}")
    print(f"  15 * 3 = {multiply(15, 3)}")
    print(f"  100 / 4 = {divide(100, 4)}")
    print(f"  Average of [10, 20, 30] = {calculate_average([10, 20, 30])}")
    
    # Class-based interface demo
    print("\n2. Class-Based Interface Demo:")
    calc = Calculator(precision=2)
    
    print(f"  5 + 7 = {calc.add(5, 7)}")
    print(f"  12 * 3 = {calc.multiply(12, 3)}")
    print(f"  50 / 5 = {calc.divide(50, 5)}")
    
    # Chain operations demo
    print("\n3. Chain Operations Demo:")
    calc.add(100, 50)  # 150
    print(f"  Start: 100 + 50 = 150")
    print(f"  Chain mul 2 = {calc.chain_operation('mul', 2)}")  # 300
    print(f"  Chain div 3 = {calc.chain_operation('div', 3)}")  # 100
    
    # History demo
    print("\n4. History:")
    for operation in calc.get_history():
        print(f"  {operation}")
    
    print("\n" + "=" * 40)
    print("Demo completed!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
