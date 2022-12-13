from lexer import tokens
from common import *
from symbol_table import Scope

def p_if(parser):
  'if : IF OPEN_PAREN boolean_expression CLOSE_PAREN THEN body else END'
  condition = parser[3]
  body = parser[6]
  _else = parser[7]

  new_if_scope = Scope()

  if _else is None:
    node = If(condition, body, new_if_scope)
    parser[0] = node
    return
  
  new_else_scope = Scope()

  node = IfElse(condition, body, _else, new_if_scope, new_else_scope)
  parser[0] = node

  # childrens = [condition, body]
  # if _else is not None:
  #   childrens.append(_else)
  
  # parser[0] = create_node_with_childrens('if', childrens)

def p_else(parser):
  '''
  else : ELSE body
       | empty
  '''
  if len(parser) == 2:
    parser[0] = None
    return

  body = parser[2]
  parser[0] = body
  # parser[0] = create_node_with_one_children('else', body)

class If:
  def __init__(self, condition, body, scope):
    self.condition = condition
    self.body = body
    self.scope = scope

  def generate_code(self, scope):
    condition_code = self.condition.generate_code(scope)
    body_code = self.body.generate_code(scope)

    # if_code = [f'\n{create_label()}']
    if_code = []
    if_code.append('\n\t')
    if_code.extend(condition_code)
    if_code.append('\n\t')
    if_code.append(f'CMP {int(1)}')
    if_code.append('\n\t')
    false_label = create_label()
    true_label = create_label()
    if_code.append(f'JZ {true_label}')
    if_code.append('\n\t')
    if_code.append(f'JNP {false_label}')
    if_code.append('\n')
    if_code.append(true_label)
    if_code.append('\n\t')
    if_code.extend(body_code)
    if_code.append('\n')
    if_code.append(false_label)
    return if_code

class IfElse:
  def __init__(self, condition, true, false):
    self.condition = condition
    self.true = true
    self.false = false

  def generate_code(self, scope):
    condition_code = self.condition.generate_code(scope)
    true_code = self.true.generate_code(scope)
    false_code = self.false.generate_code(scope)

    if_else_code = []
    if_else_code.append('\n\t')
    if_else_code.extend(condition_code)
    if_else_code.append('\n\t')
    if_else_code.append(f'CMP {int(1)}')
    if_else_code.append('\n\t')
    false_label = create_label()
    true_label = create_label()
    if_else_code.append(f'JZ {true_label}')
    if_else_code.append('\n\t')
    if_else_code.append(f'JNP {false_label}')
    continue_label = create_label()
    if_else_code.append('\n')
    if_else_code.append(true_label)
    if_else_code.append('\n\t')
    if_else_code.extend(true_code)
    if_else_code.append('\n\t')
    if_else_code.append(f'JP {continue_label}')
    if_else_code.append('\n')
    if_else_code.append(false_label)
    if_else_code.append('\n\t')
    if_else_code.extend(false_code)
    if_else_code.append('\n')
    if_else_code.append(f'\n{continue_label}')
    return if_else_code
