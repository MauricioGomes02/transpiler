from lexer import create_lexer, tokens
from ply import yacc
from symbol_table import add_symbol, get_symbol
from assign import p_assign, Assign
from procedure import p_procedure, p_procedure_declaration
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
    for statement in statements:
        program.extend(statement.generate_code())

    program_string = ''

    for command in program:
        program_string = program_string + command

    program_string = program_string + '\n\tHALT'

    return program_string


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
    file = "TO mauricio :arroz :feijao"
    file = file + "\n"
    file = file + "count = 1"
    file = file + "\n"
    file = file + "count = 1"
    file = file + "\n"
    file = file + "count = 2"
    file = file + "\n"
    file = file + "count = 5"
    file = file + "\n"
    file = file + "END"
    program = parser.parse(file, lexer=lexer)
    # print(json.dumps(program, default=lambda o: o.__dict__, indent=4))
