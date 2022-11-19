from ply import lex
from ply.lex import TOKEN

class IllegalCharacter(Exception):
    def __init__(self, char, line):
        super().__init__(f"Illegal character: '{char}', at line {line}")

tokens = (
  "NUMBER",
  'IDENTIFIER'
)

literals = ['=', '+', '-', '*', '/', '(', ')', '^']

regular_expressions = {
  "NUMBER" : r"[+-]?\d+([.]\d*)?",
  "IGNORE" : ' \t\r',
  "IDENTIFIER" : r"[_a-zA-Z][_a-zA-Z0-9]*",
  "NEW_LINE" : r"\n+"
}

t_ignore = regular_expressions['IGNORE']

def t_error(token):
    """Report lexer error."""
    raise IllegalCharacter(token.value[0], token.lexer.lineno)

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

def lexer():
    return lex.lex()