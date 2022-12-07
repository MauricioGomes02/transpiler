from symbol_table import get_symbol
from binary_operation import BinaryOperation
from unary_operation import UnaryOperation
from number import Number
from variable import Variable


def p_expression(parser):
    '''expression : number_expression
                  | boolean_expression
    '''
    # expression = parser[1]
    # parser[0] = create_node_with_one_children('expression', expression)

    expression = parser[1]
    parser[0] = expression


def p_number_expression(parser):
    '''
    number_expression : number_expression PLUS number_expression
                      | number_expression MINUS number_expression
                      | number_expression TIMES number_expression
                      | number_expression DIVIDE number_expression
                      | number_expression POWER number_expression
    '''
    # expression_left = parser[1]
    # operator = parser[2]
    # operator_leaf = create_leaf('operator', value=operator)
    # expression_right = parser[3]

    # childrens = [expression_left, operator_leaf, expression_right]
    # parser[0] = create_node_with_childrens('number_expression', childrens)
    left = parser[1]
    operator = parser[2]
    right = parser[3]
    node = BinaryOperation(operator, left, right)
    parser[0] = node


def p_number_expression_group(parser):
    'number_expression : OPEN_PAREN number_expression CLOSE_PAREN'
    expression = parser[2]
    parser[0] = expression

# def p_number_expression_minus(parser):
#   'number_expression : MINUS number_expression'
#   operator = parser[1]
#   minus_operator_leaf = create_leaf('operator', value=operator)
#   number_expression = parser[2]
#   childrens = [minus_operator_leaf, number_expression]
#   parser[0] = create_node_with_childrens('number_expression', childrens)


def p_number_expression_minus(parser):
    'number_expression : MINUS number_expression %prec UMINUS'
    # operator = parser[1]
    # minus_operator_leaf = create_leaf('operator', value=operator)
    # number_expression = parser[2]
    # childrens = [minus_operator_leaf, number_expression]
    # parser[0] = create_node_with_childrens('number_expression', childrens)
    operator = parser[1]
    expression = parser[2]
    node = UnaryOperation(operator, expression)

    parser[0] = node


def p_number_expression_number(parser):
    'number_expression : NUMBER'
    # number = parser[1]
    # number_leaf = create_leaf("number", value=number)
    # parser[0] = create_node_with_one_children('number_expression', number_leaf)
    number = parser[1]
    leaf = Number(number)

    parser[0] = leaf


def p_number_expression_identifier(parser):
    'number_expression : VARIABLE'
    # variable = parser[1]
    # identifier = variable[1:]
    # identifier_leaf = create_leaf('identifier', value=identifier)

    # parser[0] = create_node_with_one_children('variable_expression', identifier_leaf)
    variable = parser[1]
    identifier = variable[1:]

    leaf = Variable(variable, identifier)
    parser[0] = leaf


def p_boolean_expression(parser):
    'boolean_expression : condition'
    condition = parser[1]
    parser[0] = create_node_with_one_children('boolean_expression', condition)


def p_boolean_expression_identifier(parser):
    'boolean_expression : VARIABLE'
    variable = parser[1]
    identifier = variable[1:]
    identifier_leaf = create_leaf('identifier', value=identifier)

    parser[0] = create_node_with_one_children('variable_expression', identifier_leaf)


def p_condition(parser):
    '''
    condition : condition_value condition_prime
              | NOT condition_value
    '''
    first_element = parser[1]

    if first_element == 'NOT':
        operator_leaf = create_leaf('operator', value=first_element)
        condition_value = parser[2]
        childrens = [operator_leaf, condition_value]
        parser[0] = create_node_with_childrens('condition', childrens)
        return

    condition_prime = parser[2]
    if condition_prime is not None:
        condition = [first_element]
        for condition_value in get_childrens(condition_prime):
            condition.append(condition_value)

        parser[0] = create_node_with_childrens('condition', condition)
        return

    parser[0] = create_node_with_one_children('condition', first_element)


def p_condition_group(parser):
    'condition : OPEN_PAREN condition CLOSE_PAREN'
    condition = parser[2]
    parser[0] = condition


def p_condition_prime(parser):
    '''
    condition_prime : AND condition_value
                    | OR condition_value
                    | empty
    '''
    if len(parser) == 2:
        parser[0] = None
        return

    operator = parser[1]
    operator_leaf = create_leaf('operator', value=operator)
    condition_value = parser[2]
    childrens = [operator_leaf, condition_value]
    parser[0] = create_node_with_childrens('condition_prime', childrens)


def p_condition_value(parser):
    '''
    condition_value : number_expression GT number_expression
                    | number_expression GTE number_expression
                    | number_expression LT number_expression
                    | number_expression LTE number_expression
                    | number_expression EQUALS number_expression
                    | number_expression NOT_EQUALS number_expression
    '''
    number_expression_left = parser[1]
    operator = parser[2]
    operator_leaf = create_leaf('operator', value=operator)
    number_expression_right = parser[3]
    childrens = [number_expression_left, operator_leaf, number_expression_right]
    parser[0] = create_node_with_childrens('condition_value', childrens)


def p_optional_arguments(parser):
    '''
    optional_arguments : optional_argument optional_arguments
                       | empty
    '''
    parser[0] = create_list_node(parser, 'optional_arguments')


def p_optional_argument(parser):
    'optional_argument : expression'
    expression = parser[1]
    parser[0] = create_node_with_one_children('optional_argument', expression)


def p_optional_parameters(parser):
    '''
    optional_parameters : optional_parameter optional_parameters
                        | empty
    '''
    parser[0] = create_list_node(parser, 'optional_parameters')


def p_optional_parameter(parser):
    'optional_parameter : VARIABLE'
    variable = parser[1]
    variable_leaf = create_leaf('variable', value=variable)
    parser[0] = create_node_with_one_children('optional_parameter', variable_leaf)


def p_body(parser):
    '''
    body : body_statement body_statements
    '''
    body_statement = parser[1]
    body_statements = parser[2]
    elements = create_node_with_one_children('body_statements', body_statement)

    if body_statements is None:
        parser[0] = create_node_with_one_children('body', elements)
        return

    for body in get_childrens(body_statements):
        elements.append(body)

    parser[0] = create_node_with_childrens('body', elements)


def p_body_statement(parser):
    '''
    body_statement : if
                   | while
                   | assign
                   | procedure
                   | procedure_declaration
    '''
    statement = parser[1]
    parser[0] = create_node_with_one_children('body_statement', statement)


def p_body_statements(parser):
    '''
    body_statements : body_statement body_statements
                      | empty
    '''
    parser[0] = create_list_node(parser, 'body_statements')

# def p_parameters(parser):
#   '''
#   parameters : parameter parameters
#              | empty
#   '''
#   create_list_node(parser, 'parameters')
# ################################################## - ##################################################
# def p_parameter(parser):
#   '''
#   parameter : expression
#   '''
#   expression = parser[1]
#   parser[0] = create_node_with_one_children('parameter', expression)
# ################################################## - ##################################################
# def p_optional_parameters(parser):
#   '''
#   optional_parameters : optional_parameter optional_parameters
#                       | empty
#   '''
#   create_list_node(parser, 'optional_parameters')
# ################################################## - ##################################################
# def p_optional_parameter(parser):
#   '''
#   optional_parameter : OPTIONAL_PARAMETER
#   '''
#   optional_parameter = parser[1]
#   parser[0] = create_leaf('optional_parameter', value=optional_parameter)
# ################################################## - ##################################################
# def p_expression_operation(parser):
#   '''
#   expression : expression PLUS expression
#              | expression MINUS expression
#              | expression TIMES expression
#              | expression DIVIDE expression
#              | expression POWER expression
#   '''
#   expression_left = parser[1]
#   operator = parser[2]
#   operator_leaf = create_leaf('operator', value=operator)
#   expression_right = parser[3]

#   operator_node_name = {
#     '+': 'expression_sum',
#     '-': 'expression_subtraction',
#     '*': 'expression_multiplication',
#     '/': 'expression_division',
#     '^': 'expression_potentiation'
#   }

#   expression_node_name = operator_node_name[operator]
#   childrens = [expression_left, operator_leaf, expression_right]
#   parser[0] = create_node_with_childrens(expression_node_name, childrens)
# ################################################## - ##################################################
# def p_expression_group(parser):
#   'expression : OPEN_PAREN expression CLOSE_PAREN'
#   expression = parser[2]
#   parser[0] = expression
# ################################################## - ##################################################
# def p_expression_number(parser):
#   'expression : NUMBER'
#   number = parser[1]
#   number_leaf = create_leaf("number", value=number)
#   parser[0] = create_node_with_one_children('expression_value', number_leaf)
# ################################################## - ##################################################
# def p_expression_identifier(parser):
#   'expression : IDENTIFIER'
#   identifier = parser[1]
#   symbol = get_symbol(identifier)
#   if symbol is None:
#      raise Exception(f'Undefined symbol: {identifier}: {parser.lineno(1)}')
#   elif symbol['type'] != 'VARIABLE' and symbol['type'] != 'BOOLEAN_VARIABLE':
#     raise Exception(f"Cannot use identifier that is different from 'variable' and 'boolean variable' types in expressions: {identifier}: {parser.lineno(1)}")
#   identifier_leaf = create_leaf("identifier", value=identifier)

#   parser[0] = create_node_with_one_children('expression_value', identifier_leaf)
# ################################################## - ##################################################
# def p_expression_optional_parameter(parser):
#   'expression : OPTIONAL_PARAMETER'
#   optional_parameter = parser[1]
#   optional_parameter_leaf = create_leaf("identifier", value=optional_parameter)

#   parser[0] = create_node_with_one_children('expression_value', optional_parameter_leaf)
# ################################################## - ##################################################
# def p_condition(parser):
#   'condition : condition_value condition_prime'
#   condition_value = parser[1]
#   condition_prime = parser[2]

#   condition_prime_childrens = get_childrens(condition_prime)
#   if condition_prime_childrens is not None:
#     conditions = [condition_value]
#     for condition_prime_children in condition_prime_childrens:
#       conditions.append(condition_prime_children)
#     parser[0] = create_node_with_childrens('condition', conditions)
#   else:
#     parser[0] = create_node_with_one_children('condition', condition_value)
# ################################################## - ##################################################
# def p_not_condition(parser):
#   'condition : NOT condition'
#   operator = parser[1]
#   operator_leaf = create_leaf('operator', value=operator)
#   condition = parser[2]
#   childrens = [operator_leaf, condition]
#   parser[0] = create_node_with_childrens('condition', childrens)
# ################################################## - ##################################################
# def p_condition_group(parser):
#   'condition : OPEN_PAREN condition CLOSE_PAREN'
#   condition = parser[2]
#   parser[0] = condition
# ################################################## - ##################################################
# def p_condition_value(parser):
#   '''
#   condition_value : expression condition_value_prime
#   '''
#   expression = parser[1]
#   condition_value_prime = parser[2]

#   if condition_value_prime is None:
#       expression_childrens = get_childrens(expression)
#       if expression_childrens is None:
#         raise Exception('Expected a boolean type identifier')
#       first_children = expression_childrens[0]
#       if first_children['name'] != "expression_value":
#         raise Exception('Expected a boolean type identifier')
#       expression_value_childrens = get_childrens(first_children)
#       if expression_value_childrens is not None:
#         first_children = expression_value_childrens[0]
#         if first_children['name'] != 'identifier':
#           raise Exception('Expected a boolean type identifier')
#         else:
#           identifier = first_children['value']['value']
#           symbol = get_symbol(identifier)
#           if symbol is None:
#             raise Exception(f'Undefined symbol: {identifier}: {parser.lineno(1)}')
#           elif symbol['type'] != 'BOOLEAN_VARIBALE':
#             raise Exception(f'Cannot use identifiers that are not boolean variables in conditions: {identifier}: {parser.lineno(1)}')
#           identifier_leaf = create_leaf("identifier", value=identifier)

#           parser[0] = create_node_with_one_children('condition_value', identifier_leaf)
#           return
#   else:
#     childrens = [expression, condition_value_prime]
#     parser[0] = create_node_with_childrens('condition_value', childrens)
# ################################################## - ##################################################
# def p_condition_value_prime(parser):
#   '''
#   condition_value_prime : GT expression
#                         | LT expression
#                         | GTE expression
#                         | LTE expression
#                         | EQUALS expression
#                         | NOT_EQUALS expression
#                         | empty
#   '''
#   if len(parser) == 2:
#     parser[0] = None
#     return

#   operator = parser[1]
#   operator_leaf = create_leaf('operator', value=operator)
#   expression = parser[2]

#   childrens = [operator_leaf, expression]
#   parser[0] = create_node_with_childrens('condition_value_prime', childrens)
# ################################################## - ##################################################
# def p_condition_prime(parser):
#   '''
#   condition_prime : AND condition_value condition_prime
#                   | OR condition_value condition_prime
#                   | empty
#   '''
#   if len(parser) == 2:
#     parser[0] = None
#     return

#   operator = parser[1]
#   operator_leaf = create_leaf('operator', value=operator)
#   condition_value = parser[2]
#   condition_prime = parser[3]
#   condition_prime_childrens = get_childrens(condition_prime)
#   childrens = [operator_leaf, condition_value]
#   if condition_prime_childrens is not None:
#     childrens.append(condition_prime)
#   parser[0] = create_node_with_childrens('condition_prime', childrens)
# ################################################## - ##################################################
# def p_body(parser):
#   'body : body_statement body_statements'
#   body_statement = parser[1]
#   body_statements = parser[2]
#   body_statements_childrens = get_childrens(body_statements)
#   childrens = [body_statement]
#   if body_statements_childrens is not None:
#     for body_statements_children in body_statements_childrens:
#       childrens.append(body_statements_children)

#   parser[0] = create_node_with_childrens('body', childrens)
# ################################################## - ##################################################
# def p_body_statement(parser):
#   '''
#   body_statement : assign
#                  | procedure
#                  | if
#                  | while
#   '''
#   body = parser[1]
#   parser[0] = create_node_with_one_children('body_statement', body)
# ################################################## - ##################################################
# def p_body_statements(parser):
#   '''
#   body_statements : body_statement body_statements
#                   | empty
#   '''
#   create_list_node(parser, 'body_statements')
# ################################################## - ##################################################
# def p_boolean_expression(parser):
#   '''
#   boolean_expression : condition
#   '''
#   condition = parser[1]
#   parser[0] = create_node_with_one_children('boolean_expression', condition)
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

    return elements_new
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
################################################## - ##################################################

################################################## - ##################################################


def identifier_exists(identifier):
    symbol = get_symbol(identifier)
    return symbol is not None
################################################## - ##################################################


def get_identifier_type(identifier):
    if identifier_exists(identifier):
        symbol = get_symbol(identifier)
        return symbol['type']
    else:
        raise Exception(f"Undefined '{identifier}' identifier")
################################################## - ##################################################


def get_identifier_value(identifier):
    if identifier_exists(identifier):
        symbol = get_symbol(identifier)
        return symbol['value']
    else:
        raise Exception(f"Undefined '{identifier}' identifier")
################################################## - ##################################################


def get_identifier_lineno(identifier):
    if identifier_exists(identifier):
        symbol = get_symbol(identifier)
        return symbol['lineno']
    else:
        raise Exception(f"Undefined '{identifier}' identifier")
################################################## - ##################################################


def get_variable_type(expression):
    expression_type = get_expression_type(expression)
    return 'NUMBER_VARIABLE' if expression_type == 'number_expression' else 'BOOLEAN_VARIABLE'
################################################## - ##################################################


def get_expression_type(expression):
    childrens = get_childrens(expression)
    first_children = childrens[0]
    if get_node_name(first_children) == 'variable_expression':
        variable_expression_children = get_childrens(first_children)[0]
        identifier = get_leaf_value(variable_expression_children)
        if not (identifier_exists(identifier)):
            raise Exception(f"Undefined '{identifier}' identifier")
        else:
            identifier_type = get_identifier_type(identifier)
            return 'number_expression' if identifier_type == 'NUMBER_VARIABLE' else 'boolean_expression'
    else:
        return get_node_name(first_children)
################################################## - ##################################################


def get_node_name(node):
    return node['name']
################################################## - ##################################################


def get_leaf_value(leaf):
    return leaf['value']['value']
################################################## - ##################################################


def is_procedure_identifier(symbol):
    return symbol['type'] == 'PROCEDURE'
################################################## - ##################################################


def get_optional_parameters_from_procedure(identifier):
    if not (identifier_exists(identifier)):
        raise Exception(f"Undefined '{identifier}' identifier")
    else:
        symbol = get_symbol(identifier)
        if not (is_procedure_identifier(symbol)):
            raise Exception("Expected a 'PROCEDURE' type identifier")
        else:
            return symbol['optional_parameters']
