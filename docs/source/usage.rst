Usage Guide
===========

This guide demonstrates how to use the calculator package.

Basic Operations
----------------

The calculator provides two interfaces: functional and class-based.

Functional Interface
^^^^^^^^^^^^^^^^^^^^

Simple functions for basic operations:

.. code-block:: python

   from calculator.calculator import add, divide, multiply, calculate_average
   
   # Basic arithmetic
   result = add(10, 20)        # 30
   result = multiply(5, 6)     # 30
   result = divide(100, 5)     # 20.0
   
   # Average calculation
   numbers = [10, 20, 30, 40, 50]
   avg = calculate_average(numbers)  # 30.0

Class-Based Interface
^^^^^^^^^^^^^^^^^^^^^

The Calculator class provides additional features:

.. code-block:: python

   from calculator.calculator_class import Calculator
   
   # Create instance with custom precision
   calc = Calculator(precision=3)
   
   # Basic operations
   result = calc.add(10.123, 20.456)     # 30.579
   result = calc.multiply(5.5, 6.6)      # 36.300
   
   # View operation history
   history = calc.get_history()
   for operation in history:
       print(operation)

Advanced Features
-----------------

Operation Chaining
^^^^^^^^^^^^^^^^^^

Chain operations using the previous result:

.. code-block:: python

   calc = Calculator()
   
   # Start with initial calculation
   calc.add(100, 50)              # 150
   
   # Chain operations
   calc.chain_operation("mul", 2)  # 300
   calc.chain_operation("div", 3)  # 100
   calc.chain_operation("add", 25) # 125

History Management
^^^^^^^^^^^^^^^^^^

Track and manage calculation history:

.. code-block:: python

   calc = Calculator()
   
   # Perform operations
   calc.add(10, 20)
   calc.multiply(5, 6)
   calc.divide(100, 4)
   
   # Get history
   for operation in calc.get_history():
       print(operation)
   # Output:
   # 10 + 20 = 30
   # 5 * 6 = 30
   # 100 / 4 = 25.0
   
   # Clear history
   calc.clear_history()

Error Handling
--------------

The calculator handles common errors:

.. code-block:: python

   from calculator.calculator import divide, calculate_average
   
   # Division by zero
   try:
       result = divide(10, 0)
   except ValueError as e:
       print(f"Error: {e}")  # "Error: Cannot divide by zero"
   
   # Empty list average
   try:
       avg = calculate_average([])
   except ValueError as e:
       print(f"Error: {e}")  # "Error: Cannot calculate average of empty list"

Best Practices
--------------

1. **Choose the right interface**: Use functional interface for simple calculations, class-based for complex workflows
2. **Handle exceptions**: Always handle potential errors in production code
3. **Set appropriate precision**: Choose precision based on your requirements
4. **Use history for debugging**: The history feature helps track calculation flows
