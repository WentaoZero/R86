tokens = (
		"DOLLAR",
		"PERCENTAGE",
		"COMMA",
		"LPAREN",
		"RPAREN",
		"COLON",
		"ASTERISK",
		"DOT_LONG"
	) + (
		"HEXNUM",
		"DECNUM"
	) + (
		"REGNAME",
		"LABEL"
	) + (
		"PUSH",
		"POP",
		"MOVE",
		"UNARY_ARITH",
		"BINARY_ARITH",
		"COMPARE",
		"TEST",
		"JUMP",
		"CONDITIONAL_JUMP",
		"SHIFT",
		"LEA"
	)

t_DOLLAR     = r"\$"
t_PERCENTAGE = r"\%"
t_COMMA  = r"\,"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_COLON = r"\:"
t_ASTERISK = r"\*"

def t_DOT_LONG(t):
	r"\.long\b"
	return t

def t_HEXNUM(t):
	r"\b(-?0x[0-9a-fA-F]+)\b"
	t.value = int(t.value, 16)
	return t

def t_DECNUM(t):
	r"\b(-?[0-9]+)\b"
	t.value = int(t.value, 10)
	return t

def t_REGNAME(t):
	r"\b(eax|ecx|edx|ebx|esi|edi|esp|ebp)\b"
	return t

def t_LABEL(t):
	r"\.[a-zA-Z]+[a-zA-Z0-9]*\b"
	return t

def t_PUSH(t):
	r"\b(pushl)\b"
	return t

def t_POP(t):
	r"\b(popl)\b"
	return t

def t_MOVE(t):
	r"\b(movl)\b"
	return t

def t_UNARY_ARITH(t):
	r"\b(incl|decl|negl|notl)\b"
	return t

def t_BINARY_ARITH(t):
	r"\b(addl|subl|imull|xorl|orl|andl)\b"
	return t

def t_COMPARE(t):
	r"\b(cmpl)\b"
	return t

def t_TEST(t):
	r"\b(testl)\b"
	return t

def t_JUMP(t):
	r"\b(jmp)\b"
	return t

def t_CONDITIONAL_JUMP(t):
	r"\b(jne|je|jge|jg|js|jns|jle|jl)\b"
	return t

def t_SHIFT(t):
	r"\b(shll|shrl)\b"
	return t

def t_LEA(t):
	r"\b(leal)\b"
	return t

# Ignored characters
t_ignore = " \t"

def t_error(t):
	print("Illegal character '{}'".format(t.value[0]))
	exit()

# Build the lexer
import ply.lex as lex
lex.lex()

from R86 import R86
R86Processor = R86()

def p_statement_compare(p):
	"statement : COMPARE source COMMA source"
	R86Processor.compare(p[1], p[2], p[4])

def p_statement_test(p):
	"statement : TEST source COMMA source"
	R86Processor.test(p[1], p[2], p[4])

def p_statement_jump(p):
	"statement : JUMP LABEL"
	R86Processor.conditional_jump(p[1], p[2])

def p_statement_conditional_jump(p):
	"statement : CONDITIONAL_JUMP LABEL"
	R86Processor.conditional_jump(p[1], p[2])

def p_statement_jump_to_table(p):
	"statement : JUMP ASTERISK LABEL LPAREN COMMA register COMMA NUMBER RPAREN"
	R86Processor.jump_to_table(p[3], R86Processor.get(p[6]))

def p_statement_label(p):
	"statement : LABEL COLON"
	#do nothing

def p_statement_label_in_table(p):
	"statement : DOT_LONG LABEL"
	#do nothing

def p_statement_move(p):
	"statement : MOVE source COMMA destination"
	R86Processor.set(p[2], p[4])

def p_satement_unary_arith(p):
	"statement : UNARY_ARITH destination"
	R86Processor.unary_operate(p[1], p[2])

def p_statement_binary_arith(p):
	"statement : BINARY_ARITH source COMMA destination"
	R86Processor.binary_operate(p[1], p[2], p[4])

def p_statement_unary_shift(p):
	"statement : SHIFT destination"
	R86Processor.unary_operate(p[1], p[2])

def p_statement_binary_shift(p):
	"statement : SHIFT source COMMA destination"
	R86Processor.binary_operate(p[1], p[2], p[4])

def p_statement_load_effect_address(p):
	"statement : LEA effect_address COMMA register"
	R86Processor.set(p[2], p[4])

def p_source_immediate_number(p):
	"source : DOLLAR NUMBER"
	p[0] = p[2]

def p_source_register_memory(p):
	"""source : register
			  | memory"""
	p[0] = R86Processor.get(p[1])

def p_destination_register_memory(p):
	"""destination : register
				   | memory"""
	p[0] = p[1]

def p_memory_direct_addressing(p):
	"memory : NUMBER"
	p[0] = p[1]

def p_memory_register(p):
	"memory : LPAREN register RPAREN"
	p[0] = R86Processor.get(p[2])

def p_memory_number_register(p):
	"memory : NUMBER LPAREN register RPAREN"
	p[0] = p[1] + R86Processor.get(p[3])

def p_memory_double_register(p):
	"memory : LPAREN register COMMA register RPAREN"
	p[0] = R86Processor.get(p[2]) + R86Processor.get(p[4])

def p_memory_number_double_register(p):
	"memory : NUMBER LPAREN register COMMA register RPAREN"
	p[0] = p[1] + R86Processor.get(p[3]) + R86Processor.get(p[5])

def p_effect_address_num_reg(p):
	"effect_address : NUMBER LPAREN register RPAREN"
	p[0] = p[1] + R86Processor.get(p[3])

def p_effect_address_reg_reg(p):
	"effect_address : LPAREN register COMMA register RPAREN"
	p[0] = R86Processor.get(p[2]) + R86Processor.get(p[4])

def p_effect_address_reg_reg_num(p):
	"effect_address : LPAREN register COMMA register COMMA NUMBER RPAREN"
	p[0] = R86Processor.get(p[2]) + R86Processor.get(p[4]) * p[6]

def p_effect_address_num_reg_reg_num(p):
	"effect_address : NUMBER LPAREN register COMMA register COMMA NUMBER RPAREN"
	p[0] = p[1] + R86Processor.get(p[3]) + R86Processor.get(p[5]) * p[7]

def p_effect_address_num_reg_num(p):
	"effect_address : NUMBER LPAREN COMMA register COMMA NUMBER RPAREN"
	p[0] = p[1] + R86Processor.get(p[4]) * p[6]

def p_number(p):
	"""NUMBER : DECNUM
			  | HEXNUM"""
	p[0] = p[1]

def p_register(p):
	"register : PERCENTAGE REGNAME"
	p[0] = p[2]

def p_statement_push(p):
	"statement : PUSH source"
	R86Processor.set(R86Processor.get("esp")-4, "esp")
	R86Processor.set(p[2], R86Processor.get("esp"))

def p_statement_pop(p):
	"statement : POP register"
	R86Processor.set(R86Processor.get(R86Processor.get("esp")), p[2])
	R86Processor.set(R86Processor.get("esp")+4, "esp")

def p_error(p):
	print("Syntax error at: {}".format(p))
	exit()

import ply.yacc as yacc
yacc.yacc(debug=0, write_tables=0)