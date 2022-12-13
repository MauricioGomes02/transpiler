from lexer import tokens
from common import *

def p_while(parser):
  'while : WHILE OPEN_PAREN boolean_expression CLOSE_PAREN body END'
  condition = parser[3]
  body = parser[5]

  node = While(condition, body)
  parser[0] = node

  # childrens = [condition, body]
  # parser[0] = create_node_with_childrens('while', childrens)

class While:
  def __init__(self, condition, body):
    self.condition = condition
    self.body = body

  def generate_code(self, scope):
    condition_code = self.condition.generate_code(scope)
    body_code = self.body.generate_code(scope)

    start = create_label()
    while_code = [f'\n{start}']
    while_code.append('\n\t')
    while_code.extend(condition_code)
    while_code.append('\n\t')
    while_code.append(f'CMP {int(1)}')
    while_code.append('\n\t')
    false_label = create_label()
    true_label = create_label()
    while_code.append(f'JZ {true_label}')
    while_code.append('\n\t')
    while_code.append(f'JNP {false_label}')
    while_code.append('\n')
    while_code.append(true_label)
    while_code.append('\n\t')
    while_code.extend(body_code)
    while_code.append('\n\t')
    while_code.append(f'JP {start}')
    while_code.append('\n')
    while_code.append(false_label)
    return while_code


    # while_code = [f'\n{create_label()}']
    # while_code.append('\n\t')

