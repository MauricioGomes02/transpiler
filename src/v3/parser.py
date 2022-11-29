from lexer import create_lexer, tokens
from ply import yacc
from symbol_table import add_symbol, get_symbol
from assign import p_assign
from procedure import p_procedure, p_procedure_declaration
from if_statement import p_if, p_else
from while_statement import p_while
from common import *

import json

precedence = (
  ('left', 'AND', 'OR'),
  ('left', 'NOT'),
  ('left', 'EQUALS', 'NOT_EQUALS'),
  ('nonassoc', 'GT', 'LT', 'GTE', 'LTE'),
  ('left', 'PLUS', 'MINUS'),
  ('left', 'TIMES', 'DIVIDE'),
  ('right', 'POWER'),
  ('right', 'UMINUS')
)

def p_program(parser):
  'program : statement statements'
  statement = parser[1]
  statements = parser[2]
  elements = create_node_with_one_children('statements', statement)

  if statements is None:
    parser[0] = create_node_with_one_children('program', elements)
    return


  for body in get_childrens(statements):
    elements.append(body)

  parser[0] = create_node_with_childrens('program', elements)

def p_statement(parser):
  '''
  statement : assign
            | if
            | while
            | procedure
            | procedure_declaration
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
  program = parser.parse("TO mauricio :age FO :age END", lexer=lexer)
  print(json.dumps(program, indent=4))