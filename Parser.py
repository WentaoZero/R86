tokens = (
	"REGNAME",
	"DOLLAR",
    "MOV",
    "UNARY_ARITH",
    "BINARY_ARITH",
    "SHIFT",
    "LEAL",
	"PUSH",
	"POP",
    "COMMA",
    "PERCENTAGE",
    "LPAREN",
    "RPAREN",
    "DECNUM",
    "HEXNUM"
    )

t_DOLLAR     = r"\$"
t_PERCENTAGE = r"\%"
t_COMMA  = r","
t_LPAREN = r"\("
t_RPAREN = r"\)"

def t_REGNAME(t):
	r"(eax|ecx|edx|ebx|esi|edi|esp|ebp)"
	return t

def t_MOV(t):
	r"movl"
	return t

def t_UNARY_ARITH(t):
	r"(incl|decl|negl|notl)"
	return t

def t_BINARY_ARITH(t):
	r"(addl|subl|imul|xorl|orl|andl)"
	return t

def t_SHIFT(t):
	r"(sarl|sall)"
	return t

def t_LEAL(t):
	r"leal"
	return t

def t_PUSH(t):
	r"pushl"
	return t

def t_POP(t):
	r"popl"
	return t

def t_HEXNUM(t):
    r"-?0x[0-9a-fA-F]+"
    t.value = int(t.value, 16)
    return t

def t_DECNUM(t):
    r"-?[0-9]+"
    t.value = int(t.value, 10)
    return t

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

def p_statement_move_to_register(p):
    "statement : MOV source COMMA register"
    R86Processor.setRegValue(p[2], p[4])

def p_statement_move_to_memory_register(p):
    "statement : MOV source COMMA LPAREN register RPAREN"
    R86Processor.setMemory(p[2], R86Processor.getRegValue(p[5]))

def p_statement_move_to_memory_number_register(p):
    "statement : MOV source COMMA NUMBER LPAREN register RPAREN"
    R86Processor.setMemory(p[2], R86Processor.getRegValue(p[6]) + p[4])

def p_statement_move_to_memory_number(p):
    "statement : MOV source COMMA NUMBER"
    R86Processor.setMemory(p[2], p[4])

def p_statement_unary_arith(p):
	"statement : UNARY_ARITH register"
	R86Processor.unaryOperate(p[1], p[2])

def p_statement_binary_arith(p):
	"statement : BINARY_ARITH source COMMA register"
	R86Processor.binaryOperate(p[1], p[2], p[4])

def p_statement_shift(p):
	"statement : SHIFT DOLLAR NUMBER COMMA register"
	R86Processor.shiftOperate(p[1], (int)(p[3]), p[5])

def p_statement_leal_number_register(p):
	"statement : LEAL NUMBER LPAREN register RPAREN COMMA register"
	R86Processor.setRegValue(R86Processor.getRegValue(p[4])+p[2], p[7])

def p_statement_leal_register_register(p):
	"statement : LEAL LPAREN register COMMA register RPAREN COMMA register"
	R86Processor.setRegValue(R86Processor.getRegValue(p[3])+R86Processor.getRegValue(p[5]), p[8])

def p_statement_leal_register_register_number(p):
	"statement : LEAL LPAREN register COMMA register COMMA NUMBER RPAREN COMMA register"
	R86Processor.setRegValue(R86Processor.getRegValue(p[3])+R86Processor.getRegValue(p[5])*p[7], p[10])

def p_statement_leal_number_register_register_number(p):
	"statement : LEAL NUMBER LPAREN register COMMA register COMMA NUMBER RPAREN COMMA register"
	R86Processor.setRegValue(p[2]+R86Processor.getRegValue(p[4])+R86Processor.getRegValue(p[6])*p[8], p[11])

def p_statement_leal_number_register_number(p):
	"statement : LEAL NUMBER LPAREN COMMA register COMMA NUMBER RPAREN COMMA register"
	R86Processor.setRegValue(p[2]+R86Processor.getRegValue(p[5])*p[7], p[10])

def p_statement_push(p):
	"statement : PUSH source"
	R86Processor.setRegValue(R86Processor.getRegValue("esp")-4, "esp")
	R86Processor.setMemory(p[2], R86Processor.getRegValue("esp"))

def p_statement_pop(p):
	"statement : POP register"
	R86Processor.setRegValue(R86Processor.getMemory(R86Processor.getRegValue("esp")), p[2])
	R86Processor.setRegValue(R86Processor.getRegValue("esp")+4, "esp")

def p_number(p):
	"""NUMBER : DECNUM
			  | HEXNUM"""
	p[0] = p[1]

def p_source_register(p):
    "source : register"
    try:
        p[0] = R86Processor.getRegValue(p[1])
    except LookupError:
        print("Unknown register '%s'" % p[1])
        p[0] = 0

def p_source_memory_direct(p):
	"source : memory_as_source"
	p[0] = p[1]

def p_source_number(p):
    "source : DOLLAR NUMBER"
    p[0] = p[2]

def p_memory_as_source_number(p):
	"memory_as_source : NUMBER"
	p[0] = R86Processor.getMemory(p[1])

def p_memory_as_source_register(p):
	"memory_as_source : LPAREN register RPAREN"
	p[0] = R86Processor.getMemory(R86Processor.getRegValue(p[2]))

def p_memory_as_source_number_and_register(p):
	"memory_as_source : NUMBER LPAREN register RPAREN"
	p[0] = R86Processor.getMemory(p[1] + R86Processor.getRegValue(p[3]))

def p_memory_as_source_double_register(p):
	"memory_as_source : LPAREN register COMMA register RPAREN"
	p[0] = R86Processor.getMemory(p[2] + p[4])

def p_memory_as_source_number_double_register(p):
	"memory_as_source : NUMBER LPAREN register COMMA register RPAREN"
	p[0] = R86Processor.getMemory(p[1] + R86Processor.getRegValue(p[3]) + R86Processor.getRegValue(p[5]))

def p_register(p):
	"register : PERCENTAGE REGNAME"
	p[0] = p[2]

def p_expression_source(p):
	"statement : source"

def p_error(p):
    print("Syntax error at '%s'" % p.value)
    print("Something wrong with: ")
    print(p)

import ply.yacc as yacc
yacc.yacc(debug=0, write_tables=0)