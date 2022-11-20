from lexer import tokens

precedence = (
  ('left', 'PLUS', 'MINUS'),
  ('left', 'TIMES', 'DIVIDE'),
  ('right', 'POWER')
)

def p_program_statement_list(parser):
  'program : statement statement_list'
  statement_node = parser[1]
  statements_node = parser[2]
  program_node = create_node('program')

  append_node_children(program_node, statement_node)

  if statements_node is not None:
    if 'children' in statements_node:
      for statement in statements_node['children']:
        append_node_children(program_node, statement)

  parser[0] = program_node

def p_statement_list(parser):
  '''
  statement_list : statement statement_list
  statement_list : empty
  '''
  if len(parser) == 2:
    parser[0] = None
    return
  
  if len(parser) == 3:
    statement_node = parser[1]
    statement_list_node_right = parser[2]
    statement_list_node_left = create_node('statements')

    append_node_children(statement_list_node_left, statement_node)
    if statement_list_node_right is not None:
      if 'children' in statement_list_node_right:
        for statement in statement_list_node_right['children']:
          append_node_children(statement_list_node_left, statement)

    parser[0] = statement_list_node_left
    return

def p_statement(parser):
  '''
  statement : assign
            | procedure
            | statement_procedure
  '''
  operation_node = parser[1]
  statement_node = create_node('statement')
  append_node_children(statement_node, operation_node)
  parser[0] = statement_node
  
def p_assign(parser):
  'assign : IDENTIFIER ASSIGN expression'
  identifier = parser[1]
  identifier_leaf = create_leaf('identifier', value=identifier)
  assign = parser[2]
  assign_leaf = create_leaf('operator', value=assign)
  expression_node = parser[3]

  assign_node = create_node('assign')
  append_node_children(assign_node, identifier_leaf)
  append_node_children(assign_node, assign_leaf)
  append_node_children(assign_node, expression_node)

  parser[0] = assign_node

def p_expression_operation(parser):
  '''
  expression : expression PLUS expression
             | expression MINUS expression
             | expression TIMES expression
             | expression DIVIDE expression
             | expression POWER expression
  '''
  expression_node_first = parser[1]
  operator = parser[2]
  operator_leaf = create_leaf('operator', value=operator)
  expression_node_second = parser[3]

  expression_node = None

  if operator == '+':
    expression_node = create_node('expression_sum')
  elif operator == '-':
    expression_node = create_node('expression_subtraction')
  elif operator == '*':
    expression_node = create_node('expression_multiplication')
  elif operator == '/':
    expression_node = create_node('expression_division')
  elif operator == '^':
    expression_node = create_node('expression_potentiation')

  append_node_children(expression_node, expression_node_first)
  append_node_children(expression_node, operator_leaf)
  append_node_children(expression_node, expression_node_second)

  parser[0] = expression_node

def p_expression_group(parser):
  'expression : OPEN_PAREN expression CLOSE_PAREN'
  expression_node = parser[2]
  parser[0] = expression_node

def p_expression_number(parser):
  'expression : NUMBER'
  number = parser[1]
  number_leaf = create_leaf("number", value=number)
  expression_node = create_node('expression_value')
  append_node_children(expression_node, number_leaf)
  
  parser[0] = expression_node

def p_expression_identifier(parser):
  'expression : IDENTIFIER'
  identifier = parser[1]
  identifier_leaf = create_leaf("identifier", value=identifier)
  expression_node = create_node('expression_value')
  append_node_children(expression_node, identifier_leaf)

  parser[0] = expression_node

def p_procedure(parser):
  'procedure : IDENTIFIER OPEN_PAREN parameter_list CLOSE_PAREN'
  identifier = parser[1]
  identifier_leaf = create_leaf('identifier_procedure', value=identifier)
  parameters_node = parser[3]

  procedure_node = create_node('procedure')
  append_node_children(procedure_node, identifier_leaf)
  if parameters_node is not None:
    append_node_children(procedure_node, parameters_node)

  parser[0] = procedure_node

def p_parameter_list(parser):
  '''
  parameter_list : parameter parameter_list
                 | empty
  '''
  if len(parser) == 2:
    parser[0] = None
    return

  parameter_node = parser[1]
  parameter_list_node_right = parser[2]

  parameter_list_node_left = create_node('parameters')
  append_node_children(parameter_list_node_left, parameter_node)

  if parameter_list_node_right is not None:
    if 'children' in parameter_list_node_right:
      for parameter in parameter_list_node_right['children']:
        append_node_children(parameter_list_node_left, parameter)

  parser[0] = parameter_list_node_left

def p_parameter_expression(parser):
  'parameter : expression'
  expression_node = parser[1]
  parameter_leaf = create_leaf('parameter', value=expression_node)
  parser[0] = parameter_leaf

def p_statement_procedure(parser):
  'statement_procedure : TO IDENTIFIER optional_parameter_list procedure_body procedure_body_list END'
  identifier = parser[2]
  identifier_leaf = create_leaf('identifier', value=identifier)
  optional_parameter_list_node = parser[3]
  procedure_body_node = parser[4]
  procedure_body_list_node = parser[5]

  procedure_body_list_node_new = create_node('procedure_body_list')
  append_node_children(procedure_body_list_node_new, procedure_body_node)

  if procedure_body_list_node is not None:
    if 'children' in procedure_body_list_node:
      for procedure_body in procedure_body_list_node['children']:
        append_node_children(procedure_body_list_node_new, procedure_body)

  statement_procedure_node = create_node('statement_procedure')
  append_node_children(statement_procedure_node, identifier_leaf)
  append_node_children(statement_procedure_node, optional_parameter_list_node)
  append_node_children(statement_procedure_node, procedure_body_list_node_new)

  parser[0] = statement_procedure_node

def p_optional_parameter_list(parser):
  '''
  optional_parameter_list : optional_parameter optional_parameter_list
                          | empty
  '''
  if len(parser) == 2:
    parser[0] = create_node('optional_parameters')
    return

  optional_parameter_leaf = parser[1]
  optional_parameter_list_node_right = parser[2]

  optional_parameter_list_node_left = create_node('optional_parameters')
  append_node_children(optional_parameter_list_node_left, optional_parameter_leaf)

  if optional_parameter_list_node_right is not None:
    if 'children' in optional_parameter_list_node_right:
      for optional_parameter in optional_parameter_list_node_right['children']:
        append_node_children(optional_parameter_list_node_left, optional_parameter)

  parser[0] = optional_parameter_list_node_left

def p_optional_parameter(parser):
  'optional_parameter : OPTIONAL_PARAMETER'
  optional_parameter = parser[1]
  optional_parameter_leaf = create_leaf('optional_parameter', value=optional_parameter)
  parser[0] = optional_parameter_leaf

def p_procedure_body_list(parser):
  '''
  procedure_body_list : procedure_body procedure_body_list
  procedure_body_list : empty
  '''
  if len(parser) == 2:
    parser[0] = None
    return

  procedure_body_node = parser[1]
  procedure_body_list_node_right = parser[2]

  procedure_body_list_node_left = create_node('procedure_body_list')
  append_node_children(procedure_body_list_node_left, procedure_body_node)

  if procedure_body_list_node_right is not None:
    if 'children' in procedure_body_list_node_right:
      for procedure_body in procedure_body_list_node_right['children']:
        append_node_children(procedure_body_list_node_left, procedure_body)

  parser[0] = procedure_body_list_node_left

def p_procedure_body(parser):
  '''
  procedure_body : procedure
                 | IDENTIFIER OPEN_PAREN optional_parameter_list CLOSE_PAREN
  '''
  if len(parser) == 2:
    procedure_node = parser[1]
    procedure_body_node = create_node('procedure_body')
    append_node_children(procedure_body_node, procedure_node)
    parser[0] = procedure_body_node
    return 

  identifier = parser[1]
  identifier_leaf = create_leaf('identifier', value=identifier)
  optional_parameter_list_node = parser[3]

  procedure_body_node = create_node('procedure_body')
  append_node_children(procedure_body_node, identifier_leaf)
  append_node_children(procedure_body_node, optional_parameter_list_node)

  parser[0] = procedure_body_node

def p_empty(parser):
  'empty :'
  parser[0] = None

def p_error(token):
    """Provide a simple error message."""
    if token:
        raise Exception(
            f"Unexpected token:{token.lineno}: {token.type}:'{token.value}'"
        )

    raise Exception("Syntax error at EOF.")

def create_node(name):
  return dict(name=name, children=[])

def append_node_children(node, new_node):
  assert isinstance(node, dict) and "children" in node
  node["children"].append(new_node)

def create_leaf(name, **kwargs):
  return dict(name=name, value=kwargs)

from ply import yacc
from lexer import create_lexer
import json

if __name__ == "__main__":
  lexer = create_lexer()
  parser = yacc.yacc(start="program")
  program = parser.parse("mauricio = 2 + 3 mauricio(arroz) TO mauricio :arroz mauricio(:arroz) END", lexer=lexer)
  print(json.dumps(program, indent=4))