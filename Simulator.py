tokens = (
	"REGISITER",
	"DOLLAR",
	"NUMBER",
    "INSTRUCTION",
    "COMMA",
    "PERCENTAGE",
    "LPAREN",
    "RPAREN"
    )

t_DOLLAR = r"\$"
t_INSTRUCTION   = r"mov"
t_COMMA = r","
t_PERCENTAGE = r"\%"
t_LPAREN = r"\("
t_RPAREN = r"\)"

def t_NUMBER(t):
	#r"-?(\d|[a-f])+"
    r"-?[0-9a-fA-F]+"
    t.value = int(t.value, 16)
    print(t)
    print(" value : ")
    print(str(t.value))
    return t

t_REGISITER  = r"(eax|ecx|edx|ebx|esi|edi|esp|ebp)"


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

#precedence = (('left', 'PERCENTAGE', 'REGISITER'))

from R86 import R86
R86Processor = R86()

def p_statement_move(p):
    "statement : INSTRUCTION source COMMA PERCENTAGE REGISITER"
    R86Processor.setRegValue(p[5], p[2])

def p_source_register(p):
    "source : PERCENTAGE REGISITER"
    try:
        p[0] = int(R86Processor.getRegValue(p[2]))
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
	"memory : PERCENTAGE REGISITER"
	p[0] = R86Processor.getMemory(R86Processor.getRegValue(p[2]))

def p_expression_source(p):
	"statement : source"

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc(debug=0, write_tables=0)

#print(R86Processor.getMemory(1))


#yacc.parse("mov $0, %eax")
yacc.parse("mov $0, %eax")

#print(hex(234))

#yacc.parse("$f")

#R86Processor.printReg()
#yacc.parse("mov (%eax), %ebx")
#R86Processor.printReg()

#print("%eax"[1:])

print("")

#print(int("afff",16))

#R86Processor.printReg()
#R86Processor.printMemory()

