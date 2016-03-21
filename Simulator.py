tokens = (
	"REGISITER",
	"DOLLAR",
	"NUMBER",
    "INSTRUCTION",
    "COMMA",
    "LPAREN",
    "RPAREN"
    )

t_DOLLAR = r"\$"
t_INSTRUCTION   = r"mov"
t_COMMA = r","
t_LPAREN = r"\("
t_RPAREN = r"\)"

def t_NUMBER(t):
    r"-?[0-9a-fA-F]+"
    t.value = int(t.value, 16)
    return t

t_REGISITER  = r"\%(eax|ecx|edx|ebx|esi|edi|esp|ebp)"

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

from R86 import R86
R86Processor = R86()

def p_statement_move(p):
    "statement : INSTRUCTION source COMMA REGISITER"
    R86Processor.setRegValue(p[4][1:], p[2])

def p_source_register(p):
    "source : REGISITER"
    try:
        p[0] = int(R86Processor.getRegValue(p[1][1:]))
    except LookupError:
        print("Unknown register '%s'" % p[2])
        p[0] = 0

def p_source_memory_general(p):
	"source : LPAREN memory RPAREN"
	p[0] = p[2]

def p_source_number(p):
    "source : DOLLAR NUMBER"
    p[0] = p[2]

def p_memory_register(p):
	"memory : REGISITER"
	p[0] = R86Processor.getMemory(R86Processor.getRegValue(p[1][1:]))

def p_expression_source(p):
	"statement : source"

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc(debug=0, write_tables=0)

#yacc.parse("mov $0, %eax")

yacc.parse("mov $fff, %ecx")
yacc.parse("mov $123, %edx")
yacc.parse("mov (%eax), %ebx")

R86Processor.printReg()
R86Processor.printMemory()

#print(hex(234))

#yacc.parse("$f")

#R86Processor.printReg()

print("")

#print(int("afff",16))

#R86Processor.printReg()
#R86Processor.printMemory()

