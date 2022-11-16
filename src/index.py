from ply import lex
from ply import yacc
from ply.lex import TOKEN

import json

tokens = (
  "NUMBER",
  'IDENTIFIER',
  'IF',
  'THEN',
  'ELSE',
  'END'
)

literals = ['=', '+', '-', '*', '/', '(', ')', '^']

digit_re = r'([0-9])'
non_digit_re = r'([_A-Za-z])'

regular_expressions = {
  "NUMBER" : r'[+-]?({}+[.])?{}+'.format(digit_re, digit_re),
  "IGNORE" : ' \t',
  "IDENTIFIER" : r'({}({}|{})*)'.format(non_digit_re, digit_re, non_digit_re),
  "NEW_LINE" : r"\n+",
  "IF" : r"IF",
  "THEN" : r"THEN",
  "ELSE" : r"ELSE",
  "END" : r"END"
}

t_ignore = regular_expressions['IGNORE']

def t_error(token):
  print("Illegal character '{}' in {};{}".format(
    token.value[0], 
    token.lineno, 
    token.lexpos))

  token.lexer.skip(1)

@TOKEN(regular_expressions['IF'])
def t_IF(token):
  return token

@TOKEN(regular_expressions['THEN'])
def t_THEN(token):
  return token

@TOKEN(regular_expressions['ELSE'])
def t_ELSE(token):
  return token

@TOKEN(regular_expressions['END'])
def t_END(token):
  return token

@TOKEN(regular_expressions['NEW_LINE'])
def t_newline(token):
  token.lexer.lineno += len(token.value)

@TOKEN(regular_expressions['NUMBER'])
def t_NUMBER(token):
  token.value = float(token.value)
  return token

@TOKEN(regular_expressions['IDENTIFIER'])
def t_IDENTIFIER(token):
  return token

symbol_table = {}

def p_program(parser):
  '''program : statement statement_prime'''
  print("program")
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

# def p_statement_expression(parser):
#   'statement : expression'
#   print(parser[1])

def p_statement_assign(parser):
  'statement : IDENTIFIER "=" expression'
  identifier = parser[1]
  expression = parser[3]
  # symbol_table[identifier] = expression
  node = create_node("assign")
  identifier_leaf = create_leaf("identifier", value=identifier)
  append_node_children(node, identifier)
  append_node_children(node, expression)
  parser[0] = node  

def p_statement_procedure(parser):
  'statement : procedure'

def p_statement_if(parser):
  'statement : if'

def p_if(parser):
  'if : IF "(" condition ")" then_statement else_statement END'

def p_condition(parser):
  'condition : empty'

def p_then_statement(parser):
  'then_statement : THEN body'

def p_else_statement(parser):
  'else_statement : ELSE body'

def p_else_statement_empty(parser):
  'else_statement : empty'

def p_body(parser):
  'body : empty'

def p_procedure(parser):
  'procedure : IDENTIFIER procedure_arguments'
  identifier = parser[1]
  procedure_arguments = parser[2]
  print('{} {}'.format(identifier, procedure_arguments))

def p_procedure_arguments(parser):
  'procedure_arguments : NUMBER procedure_arguments'
  number = parser[1]
  number = float(number)
  procedure_arguments_right = parser[2]

  if len(procedure_arguments_right) == 0:
    parser[0] = [number]
  else:
    new_procedure_arguments = []
    for argument in procedure_arguments_right:
      new_procedure_arguments.append(argument)
    number = float(parser[1])
    new_procedure_arguments.insert(0, number)
    parser[0] = new_procedure_arguments

def p_procedure_arguments_empty(parser):
  'procedure_arguments : empty'
  parser[0] = []

def p_expression_term_expression_prime(parser):
  'expression : term expression_prime'
  # parser[0] = parser[1] + parser[2]

def p_expression_prime_sum(parser):
  'expression_prime : "+" term expression_prime'
  parser[0] = parser[2]

def p_expression_prime_subtraction(parser):
  'expression_prime : "-" term expression_prime'
  parser[0] = -parser[1]

def p_expression_prime(parser):
  'expression_prime : empty'
  parser[0] = 0

def p_term_potentiation(parser):
  'term : potentiation term_prime'
  # parser[0] = parser[1] * parser[2]

def p_term_prime_multiplication(parser):
  'term_prime : "*" potentiation term_prime'
  parser[0] = parser[2]

def p_term_prime_division(parser):
  'term_prime : "/" potentiation term_prime'
  parser[0] = 1 / parser[2]

def p_term_prime(parser):
  'term_prime : empty'
  parser[0] = 1

def p_potentiation_factor(parser):
  'potentiation : factor potentiation_prime'
  # parser[0] = parser[1] ** parser[2]


def p_potentiation_prime_factor(parser):
  'potentiation_prime : "^" factor potentiation_prime'
  # parser[0] = parser[2]
  factor_node = parser[1]
  parser[0] = factor_node

def p_potentiation_prime(parser):
  'potentiation_prime : empty'
  # parser[0] = 1

def p_factor_group(parser):
  'factor : "(" expression ")"'
  # parser[0] = parser[2]
  node = create_node("factor")
  expression_node = parser[2]
  append_node_children(node, expression_node)

def p_factor_number(parser):
  'factor : NUMBER'
  # parser[0] = float(parser[1])
  node = create_node("factor")
  number = parser[1]
  number_leaf = create_leaf("number", value=float(number))
  append_node_children(node, number_leaf)
  parser[0] = node

def p_factor_identifier(parser):
  'factor : IDENTIFIER'
  # parser[0] = float(symbol_table[parser[1]])
  node = create_node("factor")
  identifier = parser[1]
  identifier_leaf = create_leaf("identifier", value=symbol_table[identifier])
  append_node_children(node, identifier_leaf)
  parser[0] = node

def p_empty(parser):
  'empty :'
  parser[0] = None

# def p_expression_plus(parser):
#   'expression : expression "+" expression'
#   parser[0] = parser[1] + parser[3]

# def p_expression_minus(parser):
#   'expression : expression "-" expression'
#   parser[0] = parser[1] - parser[3]

# def p_expression_times(parser):
#   'expression : expression "*" expression'
#   parser[0] = parser[1] * parser[3]

# def p_expression_divide(parser):
#   'expression : expression "/" expression'
#   parser[0] = parser[1] / parser[3]

# def p_expression_uminus(parser):
#   'expression : "-" expression %prec UMINUS'
#   parser[0] = -parser[2]

# def p_expression_group(parser):
#   'expression : "(" expression ")"'
#   parser[0] = parser[2]

# def p_expression_float(parser):
#   'expression : FLOAT'
#   parser[0] = parser[1]

# def p_expression_integer(parser):
#   'expression : INTEGER'
#   parser[0] = parser[1]

# def p_expression_identifier(parser):
#   'expression : IDENTIFIER'
#   try:
#     parser[0] = symbol_table[parser[1]]
#   except LookupError:
#     print("Undefined identifier '%s'" % parser[1])
#     parser[0] = 0

def create_node(name):
  return dict(name=name, children=[])

def append_node_children(node, new_node):
  assert isinstance(node, dict) and "children" in node
  node["children"].append(new_node)

def create_leaf(name, **kwargs):
  return dict(name=name, value=kwargs)

if __name__ == "__main__":
  lexer = lex.lex()
  parser = yacc.yacc(start="program")
  program = parser.parse("a = 3", lexer=lexer, tracking=False)
  print(json.dumps(program, indent=2))