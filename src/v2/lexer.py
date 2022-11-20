tokens = [
  "NUMBER",
  "OPEN_PAREN",
  "CLOSE_PAREN",
  "PLUS",
  "MINUS",
  "TIMES",
  "DIVIDE",
  "POWER",
  "EQUALS",
  "ASSIGN",
  "COMMA",
  "TO",
  "END",
  "OPTIONAL_PARAMETER",
  "IDENTIFIER",
]

t_ignore = ' \t\r'
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_POWER = r'\^'
t_EQUALS = '=='
t_ASSIGN = '='

def t_NUMBER(token):
  r'[+-]?\d+([.]\d*)?'
  token.value = float(token.value)
  return token

def t_TO(token):
  r'TO'
  return token

def t_END(token):
  r'END'
  return token

def t_OPTIONAL_PARAMETER(token):
  r'\:[_a-zA-Z][_a-zA-Z0-9]*'
  return token

def t_IDENTIFIER(token):
  r'[_a-zA-Z][_a-zA-Z0-9]*'
  return token

def t_newline(token):
  r'\n+'
  token.lexer.lineno += len(token.value)

class IllegalCharacter(Exception):
    def __init__(self, char, line):
        super().__init__(f"Illegal character: '{char}', at line {line}")

def t_error(token):
    """Report lexer error."""
    raise IllegalCharacter(token.value[0], token.lexer.lineno)

from ply import lex

def create_lexer():
  return lex.lex()