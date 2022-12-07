from lexer import create_lexer, tokens
from ply import yacc
from symbol_table import add_symbol, get_symbol
from assign import p_assign, Assign
from procedure import p_procedure, p_procedure_declaration
from if_statement import p_if, p_else
from while_statement import p_while
from common import *
from binary_operation import BinaryOperation

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
    # print(json.dumps(statement, default=lambda o: o.__dict__, indent=4))
    statements = parser[2]
    if statements is None:
        statements = [statement]
    else:
        statements.insert(0, statement)
    # statements = statements.insert(0, statement) if statements is not None else [statement]
    parser[0] = statements

    for statement_body in statements:
        if type(statement_body) is Assign:
            print(assign(statement_body))


def assign(assign):
    identifier = assign.identifier.value
    value = assign.value
    binary_commands = binary(value)
    binary_commands.append(f'STORE {identifier}')
    return binary_commands


def binary(_binary):

    left = _binary.left

    response = []
    if type(left) == BinaryOperation:
        response.extend(binary(left))
    else:
        response.append(f'PUSH {left.value}')

    right = _binary.right
    # if type(right) == BinaryOperation:
    #     # print(json.dumps(right, default=lambda o: o.__dict__))
    #     return binary(right)
    if type(right) == BinaryOperation:
        response.extend(binary(right))
    else:
        response.append(f'PUSH {right.value}')
    operator = _binary.operator
    operators = {
        '+': 'ADD',
        '*': 'MUL',
        '-': 'SUB',
        '/': 'DIV',
    }
    response.append(f'{operators[operator]}')

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
    program = parser.parse("a = 3 * 2 + 3 - 5 * 2 b = 3 + 3", lexer=lexer)
    print(json.dumps(program, default=lambda o: o.__dict__, indent=4))
