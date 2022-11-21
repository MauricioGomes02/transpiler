from lexer import tokens
from common import *

def p_while(parser):
  'while : WHILE OPEN_PAREN condition CLOSE_PAREN body END'
  condition = parser[3]
  body = parser[5]

  childrens = [condition, body]
  parser[0] = create_node_with_childrens('while', childrens)