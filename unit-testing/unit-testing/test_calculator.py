# test_calculator.py
import pytest
from calculator import add, subtract, multiply, divide

def test_add():
  assert add(2, 3) == 5
  assert add(-1, 1) == 0
  assert add(0, 0) == 0

def test_subtract():
  assert subtract(5, 2) == 3
  assert subtract(0, 5) == -5
  assert subtract(-2, -1) == -1

def test_multiply():
  assert multiply(2, 4) == 8
  assert multiply(-3, 2) == -6
  assert multiply(0, 5) == 0

def test_divide():
  assert divide(10, 2) == 5
  assert divide(-6, 3) == -2
  assert divide(5, 2) == 2.5

def test_divide_by_zero():
  with pytest.raises(ValueError) as excinfo:
    divide(5, 0)
  assert str(excinfo.value) == "You cannot divide by zero"

""""
@pytest.mark.parametrize("a, b, resultado", [(1, 2, 3), (-1, 1, 0), (0, 0, 0)])
def test_add_parametrized(a, b, resultado):
  assert add(a, b) == resultado
"""