from variable import Variable
from number import Number
import common

class BinaryOperation:
  def __init__(self, operator, left, right):
    self.operator = operator
    self.left = left
    self.right = right

  def generate_code(self):
    left_expression_code = self.left.generate_code()
    right_expression_code = self.right.generate_code()

    binary_code = [common.create_label()]
    binary_code.extend(left_expression_code)
    binary_code.append('\n\t')
    binary_code.extend(right_expression_code)
    binary_code.append('\n\t')

    operators = {
      '+': 'ADD',
      '-': 'SUB',
      '*': 'MUL',
      '/': 'DIV'
    }

    binary_code.append(operators[self.operator])
    return binary_code