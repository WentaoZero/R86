tokens = (
	"REGNAME",
	"DOLLAR",
	"COLON",
	"LABEL",
	"JUMP",
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
t_COMMA  = r"\,"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_COLON = r"\:"

def t_LABEL(t):
	r"\.[a-zA-Z]+[a-zA-Z0-9]*"
	return t

def t_JUMP(t):
	r"jmp"
	return t

def t_REGNAME(t):
	r"(eax|ecx|edx|ebx|esi|edi|esp|ebp)"
	return t

def t_UNARY_ARITH(t):
	r"(incl|decl|negl|notl)"
	return t

def t_BINARY_ARITH(t):
	r"(movl|addl|subl|imull|xorl|orl|andl)"
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

def verifyScaleFactor(vScale):
	if vScale not in [1, 2, 4, 8]:
		print("Illegal scale factor: {}".format(vScale))
		exit()

from R86 import R86
R86Processor = R86()

def p_statement_jump_label(p):
	"statement : JUMP LABEL"
	R86Processor.set_reg(R86Processor.label_table[p[2][1:]], "eip")

def p_statement_label(p):
	"statement : LABEL COLON"
	#do nothing

def p_statement_unary_arith_reg(p):
	"statement : UNARY_ARITH register"
	R86Processor.unary_oeprate_source_reg(p[1], p[2])

def p_statement_unary_arith_memory_num(p):
	"statement : UNARY_ARITH NUMBER"
	R86Processor.unary_operate_memory_num(p[1], p[2])

def p_statement_unary_arith_memory_reg(p):
	"statement : UNARY_ARITH LPAREN register RPAREN"
	R86Processor.unary_operate_memory_reg(p[1], p[3])

def p_statement_unary_arith_memory_num_reg(p):
	"statement : UNARY_ARITH NUMBER LPAREN register RPAREN"
	R86Processor.unary_operate_memory_num_reg(p[1], p[2], p[4])

def p_statement_unary_arith_memory_reg_reg(p):
	"statement : UNARY_ARITH LPAREN register COMMA register RPAREN"
	R86Processor.unary_operate_memory_reg_reg(p[1], p[3], p[5])

def p_statement_unary_arith_memory_num_reg_reg(p):
	"statement : UNARY_ARITH NUMBER LPAREN register COMMA register RPAREN"
	R86Processor.unary_operate_memory_num_reg_reg(p[1], p[2], p[4], p[6])

def p_statement_unary_arith_memory_reg_scale(p):
	"statement : UNARY_ARITH LPAREN COMMA register COMMA NUMBER RPAREN"
	Scale = p[6]
	verifyScaleFactor(Scale)
	R86Processor.unary_operate_memory_reg_scale(p[1], p[4], Scale)

def p_statement_unary_arith_memory_num_reg_scale(p):
	"statement : UNARY_ARITH NUMBER LPAREN COMMA register COMMA NUMBER RPAREN"
	Scale = p[7]
	verifyScaleFactor(Scale)
	R86Processor.unary_operate_memory_num_reg_scale(p[1], p[2], p[5], Scale)

def p_statement_unary_arith_memory_reg_reg_scale(p):
	"statement : UNARY_ARITH LPAREN register COMMA register COMMA NUMBER RPAREN"
	Scale = p[7]
	verifyScaleFactor(Scale)
	R86Processor.unary_operate_memory_reg_reg_scale(p[1], p[3], p[5], Scale)

def p_statement_unary_arith_memory_num_reg_reg_scale(p):
	"statement : UNARY_ARITH NUMBER LPAREN register COMMA register COMMA NUMBER RPAREN"
	Scale = p[8]
	verifyScaleFactor(Scale)
	R86Processor.unary_operate_memory_num_reg_reg_scale(p[1], p[2], p[4], p[6], Scale)

def p_statement_binary_arith_register(p):
	"statement : BINARY_ARITH source COMMA register"
	R86Processor.set_reg_value_by_source(p[1], p[2], p[4])

def p_statement_binary_arith_memory_register(p):
    "statement : BINARY_ARITH source COMMA LPAREN register RPAREN"
    R86Processor.binary_operate_source_reg(p[1], p[2], p[5])

def p_statement_binary_arith_memory_register_register_scale(p):
	"statement : BINARY_ARITH source COMMA LPAREN register COMMA register COMMA NUMBER RPAREN"
	Scale = p[9]
	verifyScaleFactor(Scale)
	R86Processor.binary_operate_source_reg_reg_scale(p[1], p[2], p[5], p[7], Scale)

def p_statement_binary_arith_memory_number_register(p):
	"statement : BINARY_ARITH source COMMA NUMBER LPAREN register RPAREN"
	R86Processor.binary_operate_source_num_reg(p[1], p[2], p[4], p[6])

def p_statement_binary_arith_memory_number(p):
    "statement : BINARY_ARITH source COMMA NUMBER"
    R86Processor.binary_operate_source_num(p[1], p[2], p[4])

def p_statement_shift(p):
	"statement : SHIFT DOLLAR NUMBER COMMA register"
	R86Processor.shift_operate(p[1], p[3], p[5])

def p_statement_leal_number_register(p):
	"statement : LEAL NUMBER LPAREN register RPAREN COMMA register"
	R86Processor.lea_num_reg(p[2], p[4], p[7])

def p_statement_leal_register_register(p):
	"statement : LEAL LPAREN register COMMA register RPAREN COMMA register"
	R86Processor.lea_reg_reg(p[3], p[5], p[8])

def p_statement_leal_register_register_scale(p):
	"statement : LEAL LPAREN register COMMA register COMMA NUMBER RPAREN COMMA register"
	ScaleFactor = p[7]
	verifyScaleFactor(ScaleFactor)
	R86Processor.lea_reg_reg_num(p[3], p[5], ScaleFactor, p[10])

def p_statement_leal_number_register_register_scale(p):
	"statement : LEAL NUMBER LPAREN register COMMA register COMMA NUMBER RPAREN COMMA register"
	ScaleFactor = p[8]
	verifyScaleFactor(ScaleFactor)
	R86Processor.lea_num_reg_reg_scale(p[2], p[4], p[6], ScaleFactor, p[11])

def p_statement_leal_number_register_scale(p):
	"statement : LEAL NUMBER LPAREN COMMA register COMMA NUMBER RPAREN COMMA register"
	ScaleFactor = p[7]
	verifyScaleFactor(ScaleFactor)
	R86Processor.lea_num_reg_scale(p[2], p[5], ScaleFactor, p[10])

def p_statement_push(p):
	"statement : PUSH source"
	R86Processor.set_reg(R86Processor.get_reg("esp")-4, "esp")
	R86Processor.set_memory(p[2], R86Processor.get_reg("esp"))

def p_statement_pop(p):
	"statement : POP register"
	R86Processor.set_reg(R86Processor.get_memory(R86Processor.get_reg("esp")), p[2])
	R86Processor.set_reg(R86Processor.get_reg("esp")+4, "esp")

def p_number(p):
	"""NUMBER : DECNUM
			  | HEXNUM"""
	p[0] = (int)(p[1])

def p_source_register(p):
    "source : register"
    try:
        p[0] = R86Processor.get_reg(p[1])
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
	p[0] = R86Processor.get_memory(p[1])

def p_memory_as_source_register(p):
	"memory_as_source : LPAREN register RPAREN"
	p[0] = R86Processor.get_memory(R86Processor.get_reg(p[2]))

def p_memory_as_source_number_and_register(p):
	"memory_as_source : NUMBER LPAREN register RPAREN"
	p[0] = R86Processor.get_memory(p[1] + R86Processor.get_reg(p[3]))

def p_memory_as_source_double_register(p):
	"memory_as_source : LPAREN register COMMA register RPAREN"
	p[0] = R86Processor.get_memory(p[2] + p[4])

def p_memory_as_source_number_double_register(p):
	"memory_as_source : NUMBER LPAREN register COMMA register RPAREN"
	p[0] = R86Processor.get_memory(p[1] + R86Processor.get_reg(p[3]) + R86Processor.get_reg(p[5]))

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