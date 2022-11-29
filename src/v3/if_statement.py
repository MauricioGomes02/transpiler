from lexer import tokens
from common import *

def p_if(parser):
  'if : IF OPEN_PAREN boolean_expression CLOSE_PAREN THEN body else END'
  condition = parser[3]
  body = parser[6]
  _else = parser[7]

  childrens = [condition, body]
  if _else is not None:
    childrens.append(_else)
  
  parser[0] = create_node_with_childrens('if', childrens)

def p_else(parser):
  '''
  else : ELSE body
       | empty
  '''
  if len(parser) == 2:
    parser[0] = None
    return

  body = parser[2]
  parser[0] = create_node_with_one_children('else', body)