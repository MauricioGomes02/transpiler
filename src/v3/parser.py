from lexer import create_lexer, tokens
from ply import yacc
from symbol_table import symbol_table, ARGUMENT, Symbol, PROCEDURE, NUMBER_VARIABLE, BOOLEAN_VARIABLE, STRING_VARIABLE
from assign import p_assign, Assign
from procedure import p_procedure, p_procedure_declaration, ProcedureDeclaration, Procedure
from if_statement import p_if, p_else
from while_statement import p_while
from common import *
from binary_operation import BinaryOperation
from unary_operation import UnaryOperation
from variable import Variable

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

def generate_code(statements):
    program = []
    program.append('.START __main__')

    _data = ['.DATA']

    _code = ['.CODE']
    _main = ['DEF __main__:']
    _procedures = []

    fo_symbol = symbol_table.get_symbol('FO')
    _procedures.append('\n\n')
    _procedures.append('DEF FO:')
    _procedures.append('\n\t')
    fo_parameters = fo_symbol.optional_parameters
    for fo_parameter in fo_parameters:
        _procedures.append(f'STORE {fo_parameter}')
        
    for statement in statements:
        scope = symbol_table
        if type(statement) is Assign:
            statement.validate_symbols(scope)

            _main.append('\n\t')

            expression = statement.value
            expression_type = None
            if type(expression) is Number or type(expression) is BinaryOperation:
                expression_type = NUMBER_VARIABLE
            elif type(expression) is Variable:
                expression_symbol = symbol_table.get_symbol(expression.value)
                expression_type = expression_symbol.type
            elif type(expression) is BooleanOperation or type(expression) is RelationalOperation:
                expression_type = BOOLEAN_VARIABLE
            elif type(expression) == String:
                expression_type = STRING_VARIABLE
            symbol_table.add_symbol(Symbol(
                statement.identifier.value,
                expression_type,
                None,
                None,
                statement.identifier.line
            ))

        if type(statement) is ProcedureDeclaration:
            statement.scope.add_parent(symbol_table)
            symbol_table.add_children(statement.scope)

            parameter_names = []
            if statement.optional_parameters is not None:
                for parameter in reversed(statement.optional_parameters):
                    parameter_names.append(f'{statement.scope.identifier}_{parameter.value}')

            symbol_table.add_symbol(Symbol(
                statement.identifier.value,
                PROCEDURE,
                None,
                parameter_names,
                statement.identifier.line
            ))

            body = statement.body

            for body_statement in body.body_statements:
                if type(body_statement) is Assign:
                    expression = body_statement.value
                    expression_type = None
                    if type(expression) is Number or type(expression) is BinaryOperation:
                        expression_type = NUMBER_VARIABLE
                    elif type(expression) is Variable:
                        expression_symbol = statement.scope.get_symbol(expression.value)
                        _local_scope = statement.scope.get_parent()
                        while expression_symbol is None and _local_scope is not None:
                            expression_symbol = _local_scope.get_symbol(expression.value)
                            _local_scope = _local_scope.get_parent()
                        expression_type = expression_symbol.type
                    elif type(expression) is BooleanOperation or type(expression) is RelationalOperation:
                        expression_type = BOOLEAN_VARIABLE
                    elif type(expression) == String:
                        expression_type = STRING_VARIABLE
                    statement.scope.add_symbol(Symbol(
                        body_statement.identifier.value,
                        expression_type,
                        None,
                        None,
                        body_statement.identifier.line
                    ))
            _procedures.append('\n\n')
            _procedures.extend(statement.generate_code(statement.scope))
            continue
        
        # if type(statement) is Procedure:


        _main.extend(statement.generate_code(scope))

    _main.append('\n\tHALT')

    add_variables_in_data(symbol_table, _data)

    program.append('\n\n')
    program.extend(_data)
    program.append('\n\n')
    program.extend(_code)
    program.append('\n\n')
    program.extend(_main)
    program.extend(_procedures)

    program_string = ''

    for command in program:
        program_string = program_string + command

    return program_string

def add_variables_in_data(obj, data, identifiers = []):
    if obj is None or obj.identifier in identifiers:
        return

    identifiers.append(obj.identifier)

    values = obj.symbols.values()
    for value in values:
        if value.type is not PROCEDURE:
            data.append(f'\n\t{value.name}')

    childrens = obj.get_childrens()
    for children in childrens:
        add_variables_in_data(children, data, identifiers)

def p_program(parser):
    'program : statement statements'
    # statement = parser[1]
    # statements = parser[2]
    # elements = create_node_with_one_children('statements', statement)

    # if statements is None:
    #     parser[0] = create_node_with_one_children('program', elements)
    #     return

    # for body in get_childrens(statements):
    #     elements.append(body)

    # parser[0] = create_node_with_childrens('program', elements)

    statement = parser[1]
    statements = parser[2]
    if statements is None:
        statements = [statement]
    else:
        statements.insert(0, statement)    

    print(generate_code(statements))

    parser[0] = statements

    # _start = ['.START __main__']
    # _data = ['.DATA']
    # _main = ['.CODE \n\n']
    # _main.append('DEF _main__:\n')
    # _procedures = []

    # for statement_body in statements:
    #     _main.extend(statement_body.generate_code())
    #     # if type(statement_body) is Assign:
    #     #     _main.extend(generate_assign(statement_body))


    # # _main.append(':label_true\n')
    # # _main.append(f'\tPUSH {int(1)}\n')
    # # _main.append(':label_false\n')
    # # _main.append(f'\tPUSH {int(0)}\n\t')
    # # _main.append(':while')
    # # _main.append('\tCMP 1\n')
    # # _main.append('\tJZ :\n')
    # # _main.append('\tLOAD')

    # response = ''

    # for element in _start:
    #     response = response + element

    # response = response + '\n\n'

    # for element in _main:
    #     response = response + element

    # response = response + '\n\n'

    # for element in _procedures:
    #     response = response + element
    #     response = response + '\n\n'

    # print(response)

def generate_assign(assign):
    identifier = assign.identifier.value
    value = assign.value

    response = []
    if type(value) == BinaryOperation:
        response.extend(generate_binary_operation(value))
    elif type(value) == Variable:
        response.append(generate_variable(value))
    else:
        response.append(f'\tPUSH {value.value}\n')

    response.append(f'\tSTORE {identifier}\n')
    return response


def generate_binary_operation(binary_operation):

    left = binary_operation.left

    response = []
    left_response = []
    right_response = []

    if type(left) == BinaryOperation:
        left_response.extend(generate_binary_operation(left))
    elif type(left) == Variable:
        left_response.append(generate_variable(left))
    elif type(left) == UnaryOperation:
        left_response.extend(generate_unary_operation(left))
    else:
        left_response.append(f'\tPUSH {left.value}\n')

    right = binary_operation.right
    if type(right) == BinaryOperation:
        right_response.extend(generate_binary_operation(right))
    elif type(right) == Variable:
        right_response.append(generate_variable(right))
    elif type(right) == UnaryOperation:
        right_response.extend(generate_unary_operation(right))
    else:
        right_response.append(f'\tPUSH {right.value}\n')

    operator = binary_operation.operator

    response.extend(left_response)
    response.extend(right_response)

    if operator == '==' or operator == '<>' or operator == '>' or operator == '<' or operator == '>=' or operator == '<=':        
        response.append('\tSTORE value_temp\n')
        response.append(f'\tCMP LOAD value_temp\n')

        if operator == '==':
            response.append('\tJNZ :label_false\n')
            response.append('\tJZ :label_true\n')
        elif operator == '<>':
            response.append('\tJZ :label_false\n')
            response.append('\tJNZ :label_true\n')
        elif operator == '>':
            response.append('\tJZ :label_false\n')
            response.append('\tJLESS :label_false\n')
            response.append('\tJMORE :label_true\n')
        elif operator == '<':
            response.append('\tJZ :label_false\n')
            response.append('\tJMORE :label_false\n')
            response.append('\tJLESS :label_true\n')
        elif operator == '>=':
            response.append('\tJLESS :label_false\n')
            response.append('\tJZ :label_true\n')
            response.append('\tJMORE :label_true\n')
        elif operator == '<=':
            response.append('\tJMORE :label_false\n')
            response.append('\tJZ :label_true\n')
            response.append('\tJLESS :label_true\n')
            
        return response
    
    if operator == 'AND' or operator == 'OR':
        response.append('\t' + operator + '\n')
        return response

    operators = {
        '+': 'ADD',
        '*': 'MUL',
        '-': 'SUB',
        '/': 'DIV',
        '^': 'POWER'
    }
    response.append(f'\t{operators[operator]}\n')
    return response

def generate_variable(variable):
    return f'\tLOAD {variable.value}'

def generate_unary_operation(unary_operation):
    response = []
    if unary_operation.operator == '-':
        value = unary_operation.value
        if type(value) == BinaryOperation:
            response.extend(generate_binary_operation(value))
        elif type(value) == Variable:
            response.append(generate_variable(value))
        else:
            response.append(f'\tPUSH {value.value}')
        response.append(f'\tPUSH {float(-1)}')
        response.append('\tMUL')
        return response


def p_statement(parser):
    '''
    statement : assign
              | if
              | while
              | procedure
              | procedure_declaration
    '''
    element = parser[1]
    parser[0] = element
    # parser[0] = create_node_with_one_children('statement', element)


def p_statements(parser):
    '''
    statements : statement statements
               | empty
    '''
    # create_list_node(parser, 'statements')
    if len(parser) == 2:
        parser[0] = None
        return
    statement = parser[1]
    statements = parser[2]
    if statements is None:
        statements = [statement]
    else:
        statements.insert(0, statement)
    parser[0] = statements


if __name__ == "__main__":
    lexer = create_lexer()
    parser = yacc.yacc(start="program")
    file = "a = 5 b = :a"
    # file = file + "\n"
    # file = file + "rafael = 8"
    # file = file + "\n"
    # file = file + "TO mauricio :arroz :feijao"
    # file = file + "\n"
    # file = file + "t = 3 + 4"
    # file = file + "\n"
    # file = file + "count = 2"
    # file = file + "\n"
    # file = file + "count = 5"
    # file = file + "\n"
    # file = file + "END"
    program = parser.parse(file, lexer=lexer)
    # print(json.dumps(symbol_table, default=lambda o: o.__dict__, indent=4))
    # print(json.dumps(program, default=lambda o: o.__dict__, indent=4))
