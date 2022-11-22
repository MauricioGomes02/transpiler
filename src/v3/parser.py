from lexer import create_lexer, tokens
from ply import yacc
from symbol_table import add_symbol, get_symbol
from assign import p_assign_expression, p_assign_boolean_expression
from procedure import p_procedure, p_procedure_statement
from if_statement import p_if, p_else
from while_statement import p_while
from common import *

import json

precedence = (
  ('left', 'AND', 'OR'),
  ('left', 'NOT'),
  ('left', 'EQUALS', 'NOT_EQUALS'),
  ('left', 'GT', 'LT', 'GTE', 'LTE'),
  ('left', 'PLUS', 'MINUS'),
  ('left', 'TIMES', 'DIVIDE'),
  ('right', 'POWER')
)

def p_program(parser):
  'program : statement statements'
  statement = parser[1]
  statements = parser[2]
  statements_childrens = get_childrens(statements)
  if statements_childrens is not None:
    childrens = [statement]
    for statements_children in statements_childrens:
      childrens.append(statements_children)
    parser[0] = create_node_with_childrens('program', childrens)
  else:
    parser[0] = create_node_with_one_children('program', statement)

def p_statement(parser):
  '''
  statement : assign
            | procedure
            | procedure_statement
            | if
            | while
  '''
  element = parser[1]
  parser[0] = create_node_with_one_children('statement', element)

def p_statements(parser):
  '''
  statements : statement statements
             | empty
  '''
  create_list_node(parser, 'statements')

if __name__ == "__main__":
  lexer = create_lexer()
  parser = yacc.yacc(start="program")
  program = parser.parse("a = 14 == 3 b = a", lexer=lexer)
  print(json.dumps(program, indent=4))