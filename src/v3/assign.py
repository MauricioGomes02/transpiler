import json
from lexer import tokens
from symbol_table import add_symbol, get_symbol, NUMBER_VARIABLE, BOOLEAN_VARIABLE, STRING_VARIABLE, Symbol
from common import *
from identifier import Identifier

def p_assign(parser):
    'assign : IDENTIFIER ASSIGN expression'
    identifier = parser[1]
    expression = parser[3]

    # symbol = get_symbol(identifier)

    # if symbol is not None:
    #     _type = symbol['type']
    #     if type(expression) is BinaryOperation or type(expression) is Number:
    #         if _type != "NUMBER_VARIABLE":
    #             raise Exception(f'{identifier} symbol cannot have its type changed: {parser.lineno(1)}')
    #     if type(expression) is Variable:
    #         variable_symbol = get_symbol(expression.value)
    #         if _type != variable_symbol['type']:
    #             raise Exception(f'{identifier} symbol cannot have its type changed: {parser.lineno(1)}')
    #     elif type(expression) is BooleanOperation :
    #         if _type != "BOOLEAN_VARIABLE":
    #             raise Exception(f'{identifier} symbol cannot have its type changed: {parser.lineno(1)}')
    #     elif type(expression) is String:
    #         if _type != "STRING_VARIBALE":
    #             raise Exception(f'{identifier} symbol cannot have its type changed: {parser.lineno(1)}')
    # else:
    #     add_symbol(identifier, get_expression_type(expression), parser.lineno(1))

    identifier_leaf = Identifier(identifier, parser.lineno(1))
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

    def generate_code(self, scope):
        assign_code = []
        assign_code.extend(self.value.generate_code(scope))
        assign_code.append('\n\t')
        identifier = self.identifier.generate_code(scope)
        symbol = scope.get_symbol(identifier)
        local_scope = scope.get_parent()
        while symbol is None and local_scope is not None:
            symbol = local_scope.get_symbol(identifier)
            local_scope = local_scope.get_parent()

        if symbol is None:
            raise Exception('Undefined')
        assign_code.append(f'STORE {symbol.name}')
        return assign_code

    def validate_symbols(self, scope):
        symbol = None
        symbol = scope.get_symbol(self.identifier.value)
        local_scope = scope.parent
        while symbol is None and local_scope is not None:
            symbol = scope.get_symbol(self.identifier.value)
            local_scope = local_scope.get_parent()
        expression_type = None

        self.value.validate_symbols(scope)

        if type(self.value) is BinaryOperation or type(self.value) is Number:
            expression_type = NUMBER_VARIABLE
        elif type(self.value) is BooleanOperation or type(self.value) is RelationalOperation:
            expression_type = BOOLEAN_VARIABLE
        elif type(self.value) is Variable:
            expression_symbol = scope.get_symbol(self.value.value)
            _local_scope = scope.get_parent()
            while expression_symbol is None and _local_scope is not None:
                symbol = _local_scope.get_symbol(self.value.value)
                _local_scope = _local_scope.get_parent()
            expression_type = expression_symbol.type

        if symbol is None:
            scope.add_symbol(Symbol(
                self.identifier.value,
                expression_type,
                None,
                None,
                self.identifier.line
            ))
            return

        symbol_type = symbol.type
        if type(self.value) is BinaryOperation or type(self.value) is Number:
            if symbol_type != NUMBER_VARIABLE:
                raise Exception(f'{self.identifier.value} symbol cannot have its type changed: {self.identifier.line}')
        elif type(self.value) is BooleanOperation or type(self.value) is RelationalOperation:
            if symbol_type != BOOLEAN_VARIABLE:
                raise Exception(f'{self.identifier.value} symbol cannot have its type changed: {self.identifier.line}')
        elif type(self.value) is String:
            if symbol_type != STRING_VARIABLE:
                raise Exception(f'{self.identifier.value} symbol cannot have its type changed: {self.identifier.line}')
        elif type(self.value) is Variable:
            expression_symbol = scope.get_symbol(self.value.value)
            _local_scope = scope.get_parent()
            while expression_symbol is None and _local_scope is not None:
                symbol = _local_scope.get_symbol(self.value.value)
                _local_scope = _local_scope.get_parent()
            expression_type = expression_symbol.type

            if symbol_type != expression_type:
                raise Exception(f'{self.identifier.value} symbol cannot have its type changed: {self.identifier.line}')
