from ply import yacc

from symbol_table import add_symbol, get_symbol
from lexer import lexer, tokens

import json

def p_program(parser):
  '''program : statement statement_prime'''
  node = create_node("program")
  statement = parser[1]
  statement_prime = parser[2]
  append_node_children(node, statement)
  for statement_p in statement_prime:
    append_node_children(node, statement_p)
  parser[0] = node

def p_statement_prime(parser):
  '''statement_prime : statement statement_prime'''
  statement = parser[1]
  statement_prime = parser[2]

  new_statement_prime = [statement]
  for statement_p in statement_prime:
    new_statement_prime.insert(0, statement_p)

  parser[0] = new_statement_prime

def p_statement_prime_empty(parser):
  '''statement_prime : empty'''
  parser[0] = []

def p_statement_statement_assign(parser):
  'statement : statement_assign'
  statement_assign_node = parser[1]
  statement_node = create_node('statement')
  append_node_children(statement_node, statement_assign_node)
  parser[0] = statement_node

def p_statement_assign(parser):
  'statement_assign : IDENTIFIER "=" expression'
  identifier = parser[1]
  expression = parser[3]
  add_symbol(identifier, "VARIABLE", parser.lineno(1), value=expression)
  statement_assign_node = create_node("statement_assign")
  identifier_leaf = create_leaf("identifier", value=identifier)
  operator_leaf = create_leaf("operator", value="=")
  append_node_children(statement_assign_node, identifier_leaf)
  append_node_children(statement_assign_node, operator_leaf)
  append_node_children(statement_assign_node, expression)
  parser[0] = statement_assign_node

def p_statement_statement_procedure(parser):
  'statement : statement_procedure'
  statement_procedure_node = parser[1]
  statement_node = create_node('statement_procedure')
  append_node_children(statement_node, statement_procedure_node)

def p_procedure(parser):
  'statement_procedure : IDENTIFIER args_prime'
  identifier = parser[1]
  identifier_leaf = create_leaf('identifier', value=identifier)
  symbol = get_symbol(identifier)
  if symbol['type'] != "PROCEDURE":
    raise Exception(f"Wrong type symbol, should be 'PROCEDURE': {identifier}: {parser.lineno(1)}")

  args_prime_node = parser[2]
  optional_args_len = len(symbol["optional_args"])
  args_prime_node_len = len(args_prime_node["children"])

  if optional_args_len != args_prime_node_len:
    raise Exception(f"The {identifier} procedure requires {optional_args_len} arguments, but {args_prime_node_len} were passed: line {parser.lineno(1)}")

  statement_procedure_node = create_node('statement_procedure')
  append_node_children(statement_procedure_node, identifier_leaf)
  append_node_children(statement_procedure_node, args_prime_node)

  parser[0] = statement_procedure_node

def p_args_prime(parser):
  'args_prime : args args_prime'
  args_node = parser[1]
  args_prime_node_right = parser[2]

  optional_args_prime_node_left = create_node('args_prime')
  append_node_children(optional_args_prime_node_left, args_node)
  for optional_args_prime in args_prime_node_right['children']:
    append_node_children(optional_args_prime_node_left, optional_args_prime)
  parser[0] = optional_args_prime_node_left

def p_args_prime_empty(parser):
  'args_prime : empty'
  args_prime_node = create_node('args_prime')
  parser[0] = args_prime_node

def p_args_number(parser):
  'args : NUMBER'
  number = parser[1]
  number_leaf = create_leaf('number', value=number)
  args_node = create_node('args')
  append_node_children(args_node, number_leaf)
  parser[0] = args_node

# def p_args_identifier(parser):
#   'args : IDENTIFIER'
#   identifier = parser[1]
#   identifier_leaf = create_leaf('identifier', value=identifier)
#   args_node = create_node('args')
#   append_node_children(args_node, identifier_leaf)
#   parser[0] = args_node

def p_statement_declaration_procedure(parser):
  'statement : statement_declaration_procedure'
  declaration_procedure_node = parser[1]
  statement_node = create_node("statement")
  append_node_children(statement_node, declaration_procedure_node)
  parser[0] = statement_node

def p_declaration_procedure(parser):
  'statement_declaration_procedure : TO IDENTIFIER optional_args_prime declaration_procedure_body'
  identifier = parser[2]
  identifier_leaf = create_leaf('identifier', value=identifier)

  optional_args_prime_node = parser[3]
  optional_arg_names = []
  for optional_args in optional_args_prime_node['children']:
    optional_arg_name = optional_args['children'][0]['value']['value']
    optional_arg_names.append(optional_arg_name)
  add_symbol(identifier, "PROCEDURE", parser.lineno(2), value=None, optional_args=optional_arg_names)
  print(get_symbol(identifier))

  declaration_procedure_body_node = parser[4]

  statement_declaration_procedure = create_node('statement_declaration_procedure')
  append_node_children(statement_declaration_procedure, identifier_leaf)
  append_node_children(statement_declaration_procedure, optional_args_prime_node)
  append_node_children(statement_declaration_procedure, declaration_procedure_body_node)
  parser[0] = statement_declaration_procedure

def p_optional_args_prime(parser):
  'optional_args_prime : optional_args optional_args_prime'
  optional_args_node = parser[1]
  optional_args_prime_node_right = parser[2]

  optional_args_prime_node_left = create_node('optional_args_prime')
  append_node_children(optional_args_prime_node_left, optional_args_node)
  for optional_args_prime in optional_args_prime_node_right['children']:
    append_node_children(optional_args_prime_node_left, optional_args_prime)
  parser[0] = optional_args_prime_node_left

def p_optional_args_prime_empty(parser):
  'optional_args_prime : empty'
  optional_args_prime_node = create_node('optional_args_prime')
  parser[0] = optional_args_prime_node

def p_optional_args(parser):
  'optional_args : ":" IDENTIFIER'
  identifier = parser[2]
  identifier_leaf = create_leaf('identifier', value=identifier)
  optional_args_node = create_node('optional_args')
  append_node_children(optional_args_node, identifier_leaf)
  parser[0] = optional_args_node

def p_declaration_procedure_body(parser):
  'declaration_procedure_body : procedure_body procedure_body_prime'
  procedure_body_node = parser[1]
  procedure_body_prime_node = parser[2]
  declaration_procedure_body_node = create_node('declaration_procedure_body')
  append_node_children(declaration_procedure_body_node, procedure_body_node)

  if procedure_body_prime_node is not None:
    for procedure_body_prime in procedure_body_prime_node['children']:
      append_node_children(declaration_procedure_body_node, procedure_body_prime)

  parser[0] = declaration_procedure_body_node

# def p_procedure_body_statement_assign(parser):
#   'procedure_body : statement_assign'
#   statement_assign_node = parser[1]
#   procedure_body_node = create_node('procedure_body')
#   append_node_children(procedure_body_node, statement_assign_node)
#   parser[0] = procedure_body_node

def p_procedure_body_statement_procedure(parser):
  'procedure_body : statement_procedure'
  statement_procedure_node = parser[1]
  procedure_body_node = create_node('procedure_body')
  append_node_children(procedure_body_node, statement_procedure_node)
  parser[0] = procedure_body_node

def p_procedure_body_prime(parser):
  'procedure_body_prime : procedure_body procedure_body_prime'
  procedure_body_node = parser[1]
  procedure_body_prime_node_right = parser[2]
  procedure_body_prime_node_left = create_node('procedure_body_prime')
  append_node_children(procedure_body_prime_node_left, procedure_body_node)

  if procedure_body_prime_node_right is not None:
    for procedure_body_prime in procedure_body_prime_node_right['children']:
      append_node_children(procedure_body_prime_node_left, procedure_body_prime)

  parser[0] = procedure_body_prime_node_left

def p_procedure_body_prime_empty(parser):
  'procedure_body_prime : empty'
  parser[0] = None

# def p_declaration_procedure_body_procedure(parser):
#   'declaration_procedure_body : statement_procedure procedure_prime'
#   statement_procedure_node = parser[1]
#   procedure_prime_node_right = parser[2]
  
#   declaration_procedure_body_node = create_node('procedure_prime')
#   append_node_children(declaration_procedure_body_node, statement_procedure_node)

#   if procedure_prime_node_right is not None and "children" in procedure_prime_node_right:
#     for procedure_prime_node in procedure_prime_node_right['children']:
#       append_node_children(declaration_procedure_body_node, procedure_prime_node)

#   parser[0] = declaration_procedure_body_node

# def p_declaration_procedure_body_statement_assign(parser):
#   'declaration_procedure_body : statement_assign'
#   statement_assign_node = parser[1]
#   declaration_procedure_body_node = create_node('declaration_procedure_body')
#   append_node_children(declaration_procedure_body_node, statement_assign_node)
#   parser[0] = declaration_procedure_body_node

# def p_declaration_procedure_body_empty(parser):
#   'declaration_procedure_body : empty'
#   parser[0] = None

# def p_procedure_prime(parser):
#   'procedure_prime : statement_procedure procedure_prime'
#   statement_procedure_node = parser[1]
#   procedure_prime_node_right = parser[2]
  
#   procedure_prime_node_left = create_node('procedure_prime')
#   append_node_children(procedure_prime_node_left, statement_procedure_node)

#   for procedure_prime_node in procedure_prime_node_right['children']:
#     append_node_children(procedure_prime_node_left, procedure_prime_node)

#   parser[0] = procedure_prime_node_left

# def p_procedure_prime_empty(parser):
#   'procedure_prime : empty'
#   parser[0] = None

def p_expression_term_expression_prime(parser):
  'expression : term expression_prime'
  term_node = parser[1]
  operator_leaf = create_leaf('operator', value="+")
  expression_prime_node = parser[2]

  if "attributes" in expression_prime_node:
    attributes = expression_prime_node["attributes"]
    if "operator_value" in attributes:
      operator_leaf = create_leaf("operator", value=attributes["operator_value"])

  expression_node = create_node("expression")
  append_node_children(expression_node, term_node)
  append_node_children(expression_node, operator_leaf)
  append_node_children(expression_node, expression_prime_node)

  parser[0] = expression_node

def p_expression_prime_sum(parser):
  'expression_prime : "+" term expression_prime'
  term_node = parser[2]
  operator_leaf = create_leaf("operator", value="+")
  expression_prime_node_right = parser[3]

  expression_prime_node_left = create_node("expression_prime")
  expression_prime_node_left["attributes"] = { "operator_value": "+" }
  append_node_children(expression_prime_node_left, term_node)
  append_node_children(expression_prime_node_left, operator_leaf)
  append_node_children(expression_prime_node_left, expression_prime_node_right)

  parser[0] = expression_prime_node_left

def p_expression_prime_subtraction(parser):
  'expression_prime : "-" term expression_prime'
  term_node = parser[2]
  operator_leaf = create_leaf("operator", value="-")
  expression_prime_node_right = parser[3]

  expression_prime_node_left = create_node("expression_prime")
  expression_prime_node_left["attributes"] = { "operator_value": "-" }
  append_node_children(expression_prime_node_left, term_node)
  append_node_children(expression_prime_node_left, operator_leaf)
  append_node_children(expression_prime_node_left, expression_prime_node_right)

  parser[0] = expression_prime_node_left

def p_expression_prime(parser):
  'expression_prime : empty'
  expression_prime_leaf = create_leaf("expression_prime", value=0)
  parser[0] = expression_prime_leaf

def p_term_potentiation(parser):
  'term : potentiation term_prime'
  potentiation_node = parser[1]
  operator_leaf = create_leaf('operator', value="*")
  term_prime_node = parser[2]

  if "attributes" in term_prime_node:
    attributes = term_prime_node["attributes"]
    if "operator_value" in attributes:
      operator_leaf = create_leaf("operator", value=attributes["operator_value"])

  term_node = create_node("term")
  append_node_children(term_node, potentiation_node)
  append_node_children(term_node, operator_leaf)
  append_node_children(term_node, term_prime_node)

  parser[0] = term_node

def p_term_prime_multiplication(parser):
  'term_prime : "*" potentiation term_prime'
  potentiation_node = parser[2]
  operator_leaf = create_leaf("operator", value="*")
  term_prime_node_right = parser[3]

  term_prime_node_left = create_node("term_prime")
  term_prime_node_left["attributes"] = { "operator_value": "*" }
  append_node_children(term_prime_node_left, potentiation_node)
  append_node_children(term_prime_node_left, operator_leaf)
  append_node_children(term_prime_node_left, term_prime_node_right)

  parser[0] = term_prime_node_left

def p_term_prime_division(parser):
  'term_prime : "/" potentiation term_prime'
  potentiation_node = parser[2]
  operator_leaf = create_leaf("operator", value="/")
  term_prime_node_right = parser[3]

  term_prime_node_left = create_node("term_prime")
  term_prime_node_left["attributes"] = { "operator_value": "/" }
  append_node_children(term_prime_node_left, potentiation_node)
  append_node_children(term_prime_node_left, operator_leaf)
  append_node_children(term_prime_node_left, term_prime_node_right)

  parser[0] = term_prime_node_left

def p_term_prime(parser):
  'term_prime : empty'
  term_prime_leaf = create_leaf("term_prime", value=1)
  parser[0] = term_prime_leaf

def p_potentiation_factor(parser):
  'potentiation : factor potentiation_prime'
  factor_node = parser[1]
  operator_leaf = create_leaf('operator', value="^")
  potentiation_prime_node = parser[2]

  if "attributes" in potentiation_prime_node:
    attributes = potentiation_prime_node["attributes"]
    if "operator_value" in attributes:
      operator_leaf = create_leaf("operator", value=attributes["operator_value"])

  potentiation_node = create_node("potentiation")
  append_node_children(potentiation_node, factor_node)
  append_node_children(potentiation_node, operator_leaf)
  append_node_children(potentiation_node, potentiation_prime_node)

  parser[0] = potentiation_node

def p_potentiation_prime_factor(parser):
  'potentiation_prime : "^" factor potentiation_prime'
  factor_node = parser[2]
  operator_leaf = create_leaf("operator", value="^")
  potentiation_prime_node_right = parser[3]

  potentiation_prime_node_left = create_node("potentiation_prime")
  potentiation_prime_node_left["attributes"] = { "operator_value": "^" }
  append_node_children(potentiation_prime_node_left, factor_node)
  append_node_children(potentiation_prime_node_left, operator_leaf)
  append_node_children(potentiation_prime_node_left, potentiation_prime_node_right)

  parser[0] = potentiation_prime_node_left

def p_potentiation_prime(parser):
  'potentiation_prime : empty'
  potentiation_prime_leaf = create_leaf("potentiation_prime", value=1)
  parser[0] = potentiation_prime_leaf

def p_factor_group(parser):
  'factor : "(" expression ")"'
  factor_node = create_node("factor")
  expression_node = parser[2]
  append_node_children(factor_node, expression_node)

def p_factor_number(parser):
  'factor : NUMBER'
  factor_node = create_node("factor")
  number = parser[1]
  number_leaf = create_leaf("number", value=float(number))
  append_node_children(factor_node, number_leaf)
  parser[0] = factor_node

def p_factor_identifier(parser):
  'factor : IDENTIFIER'
  factor_node = create_node("factor")
  identifier = parser[1]
  identifier_node = create_node("identifier")
  symbol = get_symbol(identifier)
  if symbol is None:
    raise Exception(f"Undefined symbol: {identifier}: {parser.lineno(1)}")
  identifier_value_leaf = create_leaf(identifier, value=symbol["value"])
  append_node_children(identifier_node, identifier_value_leaf)
  append_node_children(factor_node, identifier_node)
  parser[0] = factor_node

def p_empty(prod):
    """empty :"""
    prod[0] = None

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

if __name__ == "__main__":
  lexer_instance = lexer()
  parser = yacc.yacc(start="program")
  program = parser.parse("TO mauricio :preto arroz = 4 FO arroz", lexer=lexer_instance, tracking=False)
  print(json.dumps(program, indent=4))