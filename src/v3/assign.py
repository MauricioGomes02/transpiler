from lexer import tokens
from symbol_table import add_symbol, get_symbol
from common import *

def p_assign_expression(parser):
  'assign : IDENTIFIER ASSIGN expression'
  print('expression')
  identifier = parser[1]
  identifier_line = parser.lineno(1)
  expression = parser[3]
  validate_identifier(identifier, identifier_line)
  expression_childrens = get_childrens(expression)
  if expression_childrens is not None:
    first_children = expression_childrens[0]
    if first_children['name'] == 'identifier':
      identifier_value = first_children['value']['value']
      identifier_symbol = get_symbol(identifier_value)
      add_symbol(identifier, identifier_symbol['type'], identifier_line, value=expression)
    else:
      add_symbol(identifier, 'VARIABLE', identifier_line, value=expression)

  identifier_leaf = create_leaf('identifier', value=identifier)
  assign = parser[2]
  assign_leaf = create_leaf('operator', value=assign)
  childrens = [identifier_leaf, assign_leaf, expression]
  parser[0] = create_node_with_childrens('assign_expression', childrens)

def p_assign_boolean_expression(parser):
  'assign : IDENTIFIER ASSIGN boolean_expression'
  identifier = parser[1]
  identifier_line = parser.lineno(1)
  expression = parser[3]
  validate_identifier(identifier, identifier_line)
  add_symbol(identifier, 'BOOLEAN_VARIABLE', identifier_line, value=expression)

  identifier_leaf = create_leaf('identifier', value=identifier)
  assign = parser[2]
  assign_leaf = create_leaf('operator', value=assign)
  childrens = [identifier_leaf, assign_leaf, expression]
  parser[0] = create_node_with_childrens('assign_boolean_expression', childrens)

def validate_identifier(identifier, line):
  symbol = get_symbol(identifier)
  if symbol is not None:
    raise Exception(f'The symbol has already been defined: {identifier}: {line}')