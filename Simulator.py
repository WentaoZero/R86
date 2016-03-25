tokens = (
	"REGISITER",
	"DOLLAR",
    "MOVINS",
	"ADDINS",
    "COMMA",
    "LPAREN",
    "RPAREN",
    "NUMBER"
    )

t_MOVINS = r"movl"
t_DOLLAR = r"\$"
t_COMMA  = r","
t_LPAREN = r"\("
t_RPAREN = r"\)"

def t_ADDINS(token):
	r"addl"
	return token

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
    "statement : MOVINS source COMMA REGISITER"
    R86Processor.setRegValue(p[2], p[4][1:])

def p_statement_add(p):
	"statement : ADDINS source COMMA REGISITER"
	R86Processor.setRegValue(p[2] + R86Processor.getRegValue(p[4][1:]), p[4][1:])

def p_source_register(p):
    "source : REGISITER"
    try:
        p[0] = int(R86Processor.getRegValue(p[1][1:]))
    except LookupError:
        print("Unknown register '%s'" % p[2])
        p[0] = 0

def p_source_memory_direct(p):
	"source : memory"
	p[0] = p[1]

def p_source_number(p):
    "source : DOLLAR NUMBER"
    p[0] = p[2]

def p_memory_number(p):
	"memory : NUMBER"
	p[0] = 0
	#p[0] = R86Processor.getMemory(p[1])

def p_memory_register(p):
	"memory : LPAREN REGISITER RPAREN"
	p[0] = R86Processor.getMemory(R86Processor.getRegValue(p[2][1:]))

def p_memory_number_and_register(p):
	"memory : NUMBER LPAREN REGISITER RPAREN"
	p[0] = R86Processor.getMemory(p[1] + R86Processor.getRegValue(p[3][1:]))

def p_memory_double_register(p):
	"memory : LPAREN REGISITER COMMA REGISITER RPAREN"
	p[0] = R86Processor.getMemory(R86Processor.getRegValue(p[2][1:]) + R86Processor.getRegValue(p[4][1:]))

def p_memory_number_double_register(p):
	"memory : NUMBER LPAREN REGISITER COMMA REGISITER RPAREN"
	p[0] = R86Processor.getMemory(p[1] + R86Processor.getRegValue(p[3][1:]) + R86Processor.getRegValue(p[5][1:]))

def p_expression_source(p):
	"statement : source"

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc(debug=0, write_tables=0)


for i in range(0,10):
	R86Processor.setMemory(i*i, i)

yacc.parse("movl $1, %eax")
yacc.parse("movl $2, %ecx")
yacc.parse("movl 1(%eax, %ecx), %esi")
yacc.parse("movl 2, %esi")

yacc.parse("addl 8(%ebp), %eax")

#yacc.parse("addl 3 %eax")


R86Processor.printReg()
#R86Processor.printMemory()

print("")




