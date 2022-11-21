from lexer import tokens
from symbol_table import add_symbol, get_symbol
from common import *

def p_procedure(parser):
  'procedure : IDENTIFIER OPEN_PAREN parameters CLOSE_PAREN'
  identifier = parser[1]
  identifier_line = parser.lineno(1)
  validate_if_not_exists_identifier(identifier, identifier_line)
  symbol = get_symbol(identifier)
  identifier_leaf = create_leaf('identifier', value=identifier)
  parameters = parser[3]

  identifier_parameters = symbol['parameters'] if symbol is not None and 'parameters' in symbol else None
  procedure_parameters = parameters['children'] if parameters is not None and 'children' in parameters else None
  validate_parameters(identifier_parameters, procedure_parameters, identifier, identifier_line)

  childrens = [identifier_leaf]
  if parameters is not None:
    childrens.append(parameters)

  parser[0] = create_node_with_childrens('procedure', childrens)
################################################## - ##################################################
def p_procedure_statement(parser):
  'procedure_statement : TO IDENTIFIER OPEN_PAREN optional_parameters CLOSE_PAREN body END'
  identifier = parser[1]
  identifier_line = parser.lineno(1)
  validate_if_exists_identifier(identifier, identifier_line)

  optional_parameters = parser[4]
  body = parser[6]

  add_symbol(identifier, 'PROCEDURE', identifier_line, value=body)

  childrens = [identifier]
  if optional_parameters is not None:
    childrens.append(optional_parameters)
  childrens.append(body)

  parser[0] = create_node_with_childrens('procedure_statement', childrens)
################################################## - ##################################################
def validate_if_not_exists_identifier(identifier, line):
  symbol = get_symbol(identifier)
  if symbol is None:
    raise Exception(f'Undefined symbol: {identifier}: {line}')
  
  if symbol['type'] != 'PROCEDURE':
    raise Exception(f'The {identifier} identifier does not store a procedure: {line}')
################################################## - ##################################################
def validate_if_exists_identifier(identifier, line):
  symbol = get_symbol(identifier)
  if symbol is not None:
    raise Exception(f'The symbol has already been defined: {identifier}: {line}')
################################################## - ##################################################
def validate_parameters(identifier_parameters, procedure_parameters, identifier, line):
  if identifier_parameters is not None and procedure_parameters is not None:
    identifier_parameters_len = len(identifier_parameters)
    procedure_parameters_len = len(procedure_parameters)
    if identifier_parameters_len != procedure_parameters_len:
      raise Exception(f'The number of arguments of a procedure must be the same number of parameters of the same: {identifier} : {line}')
 
  if identifier_parameters is not None and procedure_parameters is None:
    raise Exception(f'The number of arguments of a procedure must be the same number of parameters of the same: {identifier} : {line}')

  if identifier_parameters is None and procedure_parameters is not None:
    raise Exception(f'The number of arguments of a procedure must be the same number of parameters of the same: {identifier} : {line}')
################################################## - ##################################################