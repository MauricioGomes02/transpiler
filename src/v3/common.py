from symbol_table import get_symbol

def p_parameters(parser):
  '''
  parameters : parameter parameters
             | empty
  '''
  create_list_node(parser, 'parameters')
################################################## - ##################################################
def p_parameter(parser):
  '''
  parameter : expression
  '''
  expression = parser[1]
  parser[0] = create_node_with_one_children('parameter', expression)
################################################## - ##################################################
def p_optional_parameters(parser):
  '''
  optional_parameters : optional_parameter optional_parameters
                      | empty
  '''
  create_list_node(parser, 'optional_parameters')
################################################## - ##################################################
def p_optional_parameter(parser):
  '''
  optional_parameter : OPTIONAL_PARAMETER
  '''
  optional_parameter = parser[1]
  parser[0] = create_leaf('optional_parameter', value=optional_parameter)
################################################## - ##################################################
def p_expression_operation(parser):
  '''
  expression : expression PLUS expression
             | expression MINUS expression
             | expression TIMES expression
             | expression DIVIDE expression
             | expression POWER expression
  '''
  expression_left = parser[1]
  operator = parser[2]
  operator_leaf = create_leaf('operator', value=operator)
  expression_right = parser[3]

  operator_node_name = {
    '+': 'expression_sum',
    '-': 'expression_subtraction',
    '*': 'expression_multiplication',
    '/': 'expression_division',
    '^': 'expression_potentiation'
  }

  expression_node_name = operator_node_name[operator]
  childrens = [expression_left, operator_leaf, expression_right]
  parser[0] = create_node_with_childrens(expression_node_name, childrens)
################################################## - ##################################################
def p_expression_group(parser):
  'expression : OPEN_PAREN expression CLOSE_PAREN'
  expression = parser[2]
  parser[0] = expression
################################################## - ##################################################
def p_expression_number(parser):
  'expression : NUMBER'
  number = parser[1]
  number_leaf = create_leaf("number", value=number)
  parser[0] = create_node_with_one_children('expression_value', number_leaf)
################################################## - ##################################################
def p_expression_identifier(parser):
  'expression : IDENTIFIER'
  identifier = parser[1]
  symbol = get_symbol(identifier)
  if symbol is None:
     raise Exception(f'Undefined symbol: {identifier}: {parser.lineno(1)}')
  elif symbol['type'] != 'VARIBALE':
    raise Exception(f'Cannot use non-variable identifiers in expressions: {identifier}: {parser.lineno(1)}')
  identifier_leaf = create_leaf("identifier", value=identifier)

  parser[0] = create_node_with_one_children('expression_value', identifier_leaf)
################################################## - ##################################################
def p_expression_optional_parameter(parser):
  'expression : OPTIONAL_PARAMETER'
  optional_parameter = parser[1]
  optional_parameter_leaf = create_leaf("identifier", value=optional_parameter)

  parser[0] = create_node_with_one_children('expression_value', optional_parameter_leaf)
################################################## - ##################################################
def p_condition(parser):
  'condition : condition_value condition_prime'
  condition_value = parser[1]
  condition_prime = parser[2]

  condition_prime_childrens = get_childrens(condition_prime)
  if condition_prime_childrens is not None:
    conditions = [condition_value]
    for condition_prime_children in condition_prime_childrens:
      conditions.append(condition_prime_children)
    parser[0] = create_node_with_childrens('condition', conditions)
  else:
    parser[0] = create_node_with_one_children('condition', condition_value)
################################################## - ##################################################
def p_not_condition(parser):
  'condition : NOT condition'
  operator = parser[1]
  operator_leaf = create_leaf('operator', value=operator)
  condition = parser[2]
  childrens = [operator_leaf, condition]
  parser[0] = create_node_with_childrens('condition', childrens)
################################################## - ##################################################
def p_condition_group(parser):
  'condition : OPEN_PAREN condition CLOSE_PAREN'
  condition = parser[2]
  parser[0] = condition
################################################## - ##################################################
def p_condition_value(parser):
  '''
  condition_value : expression GT expression
                  | expression LT expression
                  | expression GTE expression
                  | expression LTE expression
                  | expression EQUALS expression
                  | expression NOT_EQUALS expression
  '''
  expression_left = parser[1]
  operator = parser[2]
  operator_leaf = create_leaf('operator', value=operator)
  expression_right = parser[3]
  childrens = [expression_left, operator_leaf, expression_right]
  parser[0] = create_node_with_childrens('condition_value', childrens)
################################################## - ##################################################
def p_condition_prime(parser):
  '''
  condition_prime : AND condition_value condition_prime
                  | OR condition_value condition_prime
                  | empty
  '''
  if len(parser) == 2:
    parser[0] = None
    return
    
  operator = parser[1]
  operator_leaf = create_leaf('operator', value=operator)
  condition_value = parser[2]
  condition_prime = parser[3]
  condition_prime_childrens = get_childrens(condition_prime)
  childrens = [operator_leaf, condition_value]
  if condition_prime_childrens is not None:
    childrens.append(condition_prime)
  parser[0] = create_node_with_childrens('condition_prime', childrens)
################################################## - ##################################################
def p_body(parser):
  'body : body_statement body_statements'
  body_statement = parser[1]
  body_statements = parser[2]
  body_statements_childrens = get_childrens(body_statements)
  childrens = [body_statement]
  if body_statements_childrens is not None:
    for body_statements_children in body_statements_childrens:
      childrens.append(body_statements_children)
  
  parser[0] = create_node_with_childrens('body', childrens)
################################################## - ##################################################
def p_body_statement(parser):
  '''
  body_statement : assign
                 | procedure   
                 | if         
  '''
  body = parser[1]
  parser[0] = create_node_with_one_children('body_statement', body)
################################################## - ##################################################
def p_body_statements(parser):
  '''
  body_statements : body_statement body_statements
                  | empty                
  '''
  create_list_node(parser, 'body_statements')
################################################## - ##################################################
def p_empty(parser):
  'empty :'
  parser[0] = None
################################################## - ##################################################
def p_error(token):
    """Provide a simple error message."""
    if token:
        raise Exception(
            f"Unexpected token:{token.lineno}: {token.type}:'{token.value}'"
        )

    raise Exception("Syntax error at EOF.")
################################################## - ##################################################

################################################## - ##################################################
def create_list_node(parser, node_name):
  if len(parser) == 2:
      parser[0] = None
      return

  element = parser[1]
  elements = parser[2]

  elements_new = create_node(node_name)
  append_node_children(elements_new, element)
  elements_childrens = get_childrens(elements)
  if elements_childrens is not None:
    for elements_children in elements_childrens:
      append_node_children(elements_new, elements_children)

  parser[0] = elements_new
################################################## - ##################################################
def create_node_with_one_children(node_name, children):
  node = create_node(node_name)
  append_node_children(node, children)
  return node
################################################## - ##################################################
def create_node_with_childrens(node_name, childrens):
  node = create_node(node_name)
  for children in childrens:
    append_node_children(node, children)
  return node
################################################## - ##################################################
def get_childrens(node):
  if node is not None and 'children' in node:
    return node['children']
  return None
################################################## - ##################################################

################################################## - ##################################################
def create_node(name):
  return dict(name=name, children=[])
################################################## - ##################################################
def append_node_children(node, new_node):
  assert isinstance(node, dict) and "children" in node
  node["children"].append(new_node)
################################################## - ##################################################
def create_leaf(name, **kwargs):
  return dict(name=name, value=kwargs)

# Lógica booleana (tentativa)
def bool(c):
    global symbol_table
    if type(c) != tuple:
        return c
    else:
        op = c[0]
        num1 = c[1]
        num2 = c[2]
        if op == '>':
            return num1 > num2
        elif op == '<':
            return num1 < num2
        elif op == '>=':
            return num1 >= num2
        elif op == '<=':
            return num1 <= num2
        elif op == '=':
            return num1 == num2
        elif op == '!=':
            return num1 != num2