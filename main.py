"""Main module using Calculator class."""

import logging

# import calculator
from src.calculator.calculator_class import Calculator

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main_functional(op: str, a: float, b: float) -> None:
    """Old main"""
    from src.calculator.calculator import add, divide, multiply

    operations = {
        "add": add,
        "mul": multiply,
        "div": divide,
    }

    try:
        result = operations[op](a, b)
        logging.info(f"Functional Result: {result}")
    except ValueError as e:
        logging.error(f"Functional Error: {e}")


def main_oop(op: str, a: float, b: float) -> None:
    """New main oop"""
    calc = Calculator(precision=2)

    operations = {
        "add": calc.add,
        "mul": calc.multiply,
        "div": calc.divide,
    }

    try:
        result = operations[op](a, b)
        logging.info(f"OOP Result: {result}")
        logging.info(f"History: {calc.get_history()}")
    except ValueError as e:
        logging.error(f"OOP Error: {e}")


def main_oop_real() -> None:
    """Main oop"""
    calc = Calculator(precision=3)

    calc.add(10, 5)  # 15
    calc.chain_operation("mul", 2)  # 30
    calc.chain_operation("div", 3)  # 10

    for op in calc.get_history():
        logging.info(f"  {op}")

    logging.info(f"Last result: {calc.last_result}")

    avg = calc.calculate_average([10, 20, 30, 40])
    logging.info(f"Media: {avg}")


if __name__ == "__main__":
    # logging.info(f"Proj: {calculator.__project__}. Version: {calculator.__version__}. Author: {calculator.__author__}")
    main_functional("add", 3, 2)
    main_functional("div", 10, 0)

    main_oop("add", 3, 2)
    main_oop("div", 10, 2)

    main_oop_real()
