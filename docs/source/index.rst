My Project Documentation
========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   modules
   classes

Project Overview
----------------

My Project is a simple calculator library with both functional and class-based interfaces.

Features
--------

- Basic arithmetic operations (add, divide, multiply)
- Average calculation
- Operation history tracking (class-based)
- Configurable precision
- Chain operations support

Installation
------------

.. code-block:: bash

   pip install -e .

Quick Start
-----------

Using functional interface:

.. code-block:: python

   from calculator.calculator import add, multiply
   
   result = add(10, 20)
   print(result)  # 30

Using class-based interface:

.. code-block:: python

   from calculator.calculator_class import Calculator
   
   calc = Calculator(precision=2)
   result = calc.add(10, 20)
   print(calc.history)  # ['10 + 20 = 30']

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
