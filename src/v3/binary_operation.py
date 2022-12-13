from variable import Variable
from number import Number
import common

class BinaryOperation:
  def __init__(self, operator, left, right):
    self.operator = operator
    self.left = left
    self.right = right

  def generate_code(self, scope):
    left_expression_code = self.left.generate_code(scope)
    right_expression_code = self.right.generate_code(scope)

    # binary_code = [f'\n{common.create_label()}']
    binary_code = []
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

  def validate_symbols(self, scope):
    if type(self.left) is Variable:
      self.validate_symbol(self.left.value, scope)
    if type(self.right) is Variable:
      self.validate_symbol(self.left.value, scope)

  def validate_symbol(name, scope):
    symbol = scope.get_symbol(name)
    local_scope = scope.parent
    while symbol is None and local_scope is not None:
      symbol = local_scope.get_symbol(name)
      local_scope = local_scope.get_parent()

    if symbol is None:
      raise Exception('Undefined')