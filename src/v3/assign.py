from lexer import tokens
from symbol_table import add_symbol, get_symbol
from common import *
from identifier import Identifier

def p_assign(parser):
    'assign : IDENTIFIER ASSIGN expression'
    identifier = parser[1]
    expression = parser[3]

    symbol = get_symbol(identifier)

    if symbol is not None:
        _type = symbol['type']
        if type(expression) is BinaryOperation or type(expression) is Number:
            if _type != "NUMBER_VARIABLE":
                raise Exception(f'{identifier} symbol cannot have its type changed: {parser.lineno(1)}')
        if type(expression) is Variable:
            variable_symbol = get_symbol(expression.value)
            if _type != variable_symbol['type']:
                raise Exception(f'{identifier} symbol cannot have its type changed: {parser.lineno(1)}')
        elif type(expression) is BooleanOperation :
            if _type != "BOOLEAN_VARIABLE":
                raise Exception(f'{identifier} symbol cannot have its type changed: {parser.lineno(1)}')
        elif type(expression) is String:
            if _type != "STRING_VARIBALE":
                raise Exception(f'{identifier} symbol cannot have its type changed: {parser.lineno(1)}')
    else:
        add_symbol(identifier, get_expression_type(expression), parser.lineno(1))

    identifier_leaf = Identifier(identifier)
    node = Assign(identifier_leaf, expression)
    parser[0] = node

    # if identifier_exists(identifier):
    #     raise Exception(f'The symbol has already been defined: {identifier}: {line}')
    # else:
    #     variable_type = get_variable_type(expression)
    #     add_symbol(identifier, variable_type, line, value=expression)

    # identifier_leaf = create_leaf('identifier', value=identifier)
    # operator = parser[2]
    # operator_leaf = create_leaf('operator', value=operator)
    # childrens = [identifier_leaf, operator_leaf, expression]
    # parser[0] = create_node_with_childrens('assign', childrens)
    

# def p_assign_expression(parser):
#   'assign : IDENTIFIER ASSIGN expression'
#   print('expression')
#   identifier = parser[1]
#   identifier_line = parser.lineno(1)
#   expression = parser[3]
#   validate_identifier(identifier, identifier_line)
#   expression_childrens = get_childrens(expression)
#   if expression_childrens is not None:
#     first_children = expression_childrens[0]
#     if first_children['name'] == 'identifier':
#       identifier_value = first_children['value']['value']
#       identifier_symbol = get_symbol(identifier_value)
#       add_symbol(identifier, identifier_symbol['type'], identifier_line, value=expression)
#     else:
#       add_symbol(identifier, 'VARIABLE', identifier_line, value=expression)

#   identifier_leaf = create_leaf('identifier', value=identifier)
#   assign = parser[2]
#   assign_leaf = create_leaf('operator', value=assign)
#   childrens = [identifier_leaf, assign_leaf, expression]
#   parser[0] = create_node_with_childrens('assign_expression', childrens)

# def p_assign_boolean_expression(parser):
#   'assign : IDENTIFIER ASSIGN boolean_expression'
#   identifier = parser[1]
#   identifier_line = parser.lineno(1)
#   expression = parser[3]
#   validate_identifier(identifier, identifier_line)
#   add_symbol(identifier, 'BOOLEAN_VARIABLE', identifier_line, value=expression)

#   identifier_leaf = create_leaf('identifier', value=identifier)
#   assign = parser[2]
#   assign_leaf = create_leaf('operator', value=assign)
#   childrens = [identifier_leaf, assign_leaf, expression]
#   parser[0] = create_node_with_childrens('assign_boolean_expression', childrens)

# def validate_identifier(identifier, line):
#   symbol = get_symbol(identifier)
#   if symbol is not None:
#     raise Exception(f'The symbol has already been defined: {identifier}: {line}')

def get_expression_type(expression):
    if type(expression) is Number or type(expression) is BinaryOperation:
        return 'NUMBER_VARIABLE'
    elif type(expression) is Variable:
        symbol = get_symbol(expression.value)
        return symbol['type']
    elif type(expression) is BooleanOperation or type(expression) is RelationalOperation:
        return 'BOOLEAN_VARIABLE'
    elif type(expression) == String:
        return 'STRING_VARIABLE'

class Assign:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def generate_code(self):
        assign_code = []
        assign_code.extend(self.value.generate_code())
        # if type(self.value) is BooleanOperation or type(self.value) is RelationalOperation:
        #     assign_code.append('\n')
        #     assign_code.append(create_label())
        assign_code.append('\n\t')
        assign_code.append(f'STORE {self.identifier.generate_code()}')
        return assign_code
