from lexer import tokens
from symbol_table import Scope, symbol_table, Symbol, PROCEDURE, NUMBER_VARIABLE, STRING_VARIABLE, BOOLEAN_VARIABLE, ARGUMENT
from identifier import Identifier
from assign import Assign
from common import *

def p_procedure(parser):
  'procedure : IDENTIFIER optional_arguments'
  identifier = parser[1]
  optional_arguments = parser[2]

  identifier_node = Identifier(identifier, parser.lineno(1))
  node = Procedure(
    identifier_node, 
    optional_arguments)

  parser[0] = node
  # identifier_leaf = create_leaf('identifier', value=identifier)
  # line = parser.lineno(1)
  # optional_arguments = parser[2]
  # childrens = [identifier_leaf]

  # if not(identifier_exists(identifier)):
  #   raise Exception(f"Undefined '{identifier}' identifier: {line}")
  # else:
  #   optional_parameters = get_optional_parameters_from_procedure(identifier)
  #   if optional_parameters is not None:
  #     optional_parameters_len = len(optional_parameters)
  #     if optional_arguments is None or optional_parameters_len != len(get_childrens(optional_arguments)):
  #       raise Exception(f'The number of arguments of a procedure must be the same number of parameters of the same: {identifier} : {line}')
  #     childrens.append(optional_arguments)
  #   else:
  #     if optional_arguments is not None:
  #       raise Exception(f'The number of arguments of a procedure must be the same number of parameters of the same: {identifier} : {line}')

  #   parser[0] = create_node_with_childrens('procedure', childrens)

def p_procedure_declaration(parser):
  'procedure_declaration : TO IDENTIFIER optional_parameters body END'
  identifier = parser[2]
  optional_parameters = parser[3]
  body = parser[4]

  new_scope = Scope()
  if optional_parameters is not None:
    for optional_parameter in optional_parameters:
      new_scope.add_symbol(Symbol(
        optional_parameter.value,
        ARGUMENT,
        None,
        None,
        None
      ))

  identifier_node = Identifier(identifier, parser.lineno(2))
  node = ProcedureDeclaration(
    identifier_node, 
    optional_parameters, 
    body,
    new_scope)
  parser[0] = node

class Procedure:
  def __init__(self, identifier, optional_arguments):
    self.identifier = identifier
    self.optional_arguments = optional_arguments

  def generate_code(self, scope):
    procedure_code = []

    identifier = self.identifier.generate_code(scope)
    symbol = scope.get_symbol(identifier)
    local_scope = scope.get_parent()
    while symbol is None and local_scope is not None:
        symbol = local_scope.get_symbol(identifier)
        local_scope = local_scope.get_parent()

    for argument in reversed(self.optional_arguments):
      procedure_code.append('\n\t')
      procedure_code.extend(argument.generate_code(scope))
    
    procedure_code.append('\n\t')
    procedure_code.append(f'CALL {identifier}')

    return procedure_code

class ProcedureDeclaration:
  def __init__(self, identifier, optional_parameters, body, scope):
    self.identifier = identifier
    self.optional_parameters = optional_parameters
    self.body = body
    self.scope = scope

  def generate_code(self, scope):
    procedure_declaration_code = ['\n']
    procedure_declaration_code.append(f'DEF {self.identifier.generate_code(scope)}:')

    symbol = scope.get_symbol(self.identifier.value)
    local_scope = scope.get_parent()
    while symbol is None and local_scope is not None:
        symbol = local_scope.get_symbol(self.identifier.value)
        local_scope = local_scope.get_parent()

    optional_parameters = symbol.optional_parameters

    for optional_parameter in reversed(optional_parameters):
      procedure_declaration_code.append('\n\t')
      procedure_declaration_code.append(f'STOR {optional_parameter}')

    body_code = self.body.generate_code(scope)
    procedure_declaration_code.extend(body_code)

    return procedure_declaration_code

  # identifier = parser[2]
  # identifier_leaf = create_leaf("identifier", value=identifier)
  # childrens = [identifier_leaf]
  # line = parser.lineno(2)
  # if identifier_exists(identifier):
  #   raise Exception(f'The symbol has already been defined: {identifier}: {line}')
  # else:
  #   optional_parameters = parser[3]
  #   if optional_parameters is None:
  #     add_symbol(identifier, 'PROCEDURE', line, value=None, optional_parameters=None)
  #   else:
  #     parameters = []
  #     for parameter in get_childrens(optional_parameters):
  #       vaiable_name = get_leaf_value(get_childrens(parameter)[0])
  #       parameters.append(f'{identifier}.{vaiable_name[1:]}')
  #     add_symbol(identifier, 'PROCEDURE', line, value=None, optional_parameters=parameters)
  #     print(get_symbol(identifier))
  #     childrens.append(optional_parameters)

  # body = parser[4]
  # childrens.append(body)
  
  # parser[0] = create_node_with_childrens('procedure_declaration', childrens)

# def p_procedure(parser):
#   'procedure : IDENTIFIER OPEN_PAREN parameters CLOSE_PAREN'
#   identifier = parser[1]
#   identifier_line = parser.lineno(1)
#   validate_if_not_exists_identifier(identifier, identifier_line)
#   symbol = get_symbol(identifier)
#   identifier_leaf = create_leaf('identifier', value=identifier)
#   parameters = parser[3]

#   identifier_parameters = symbol['parameters'] if symbol is not None and 'parameters' in symbol else None
#   procedure_parameters = parameters['children'] if parameters is not None and 'children' in parameters else None
#   validate_parameters(identifier_parameters, procedure_parameters, identifier, identifier_line)

#   childrens = [identifier_leaf]
#   if parameters is not None:
#     childrens.append(parameters)

#   parser[0] = create_node_with_childrens('procedure', childrens)
# ################################################## - ##################################################
# def p_procedure_statement(parser):
#   'procedure_statement : TO IDENTIFIER OPEN_PAREN optional_parameters CLOSE_PAREN body END'
#   identifier = parser[1]
#   identifier_line = parser.lineno(1)
#   validate_if_exists_identifier(identifier, identifier_line)

#   optional_parameters = parser[4]
#   body = parser[6]

#   add_symbol(identifier, 'PROCEDURE', identifier_line, value=body)

#   childrens = [identifier]
#   if optional_parameters is not None:
#     childrens.append(optional_parameters)
#   childrens.append(body)

#   parser[0] = create_node_with_childrens('procedure_statement', childrens)
# ################################################## - ##################################################
# def validate_if_not_exists_identifier(identifier, line):
#   symbol = get_symbol(identifier)
#   if symbol is None:
#     raise Exception(f'Undefined symbol: {identifier}: {line}')
  
#   if symbol['type'] != 'PROCEDURE':
#     raise Exception(f'The {identifier} identifier does not store a procedure: {line}')
# ################################################## - ##################################################
# def validate_if_exists_identifier(identifier, line):
#   symbol = get_symbol(identifier)
#   if symbol is not None:
#     raise Exception(f'The symbol has already been defined: {identifier}: {line}')
# ################################################## - ##################################################
# def validate_parameters(identifier_parameters, procedure_parameters, identifier, line):
#   if identifier_parameters is not None and procedure_parameters is not None:
#     identifier_parameters_len = len(identifier_parameters)
#     procedure_parameters_len = len(procedure_parameters)
#     if identifier_parameters_len != procedure_parameters_len:
#       raise Exception(f'The number of arguments of a procedure must be the same number of parameters of the same: {identifier} : {line}')
 
#   if identifier_parameters is not None and procedure_parameters is None:
#     raise Exception(f'The number of arguments of a procedure must be the same number of parameters of the same: {identifier} : {line}')

#   if identifier_parameters is None and procedure_parameters is not None:
#     raise Exception(f'The number of arguments of a procedure must be the same number of parameters of the same: {identifier} : {line}')
# ################################################## - ##################################################