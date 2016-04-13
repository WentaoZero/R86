from Register import SegmentRegister, IntegerRegister, SpecialRegister
from Memory  import Memory

class R86:
	def __init__(self):
		self.segment_register = SegmentRegister()
		self.integer_register = IntegerRegister()
		self.special_register = SpecialRegister()
		self.memory = Memory()

		self.code_segment    = []
		self.label_table     = {}

		self.unary_operation_dict = {}
		self.unary_operation_dict["incl"] = lambda x: x + 1
		self.unary_operation_dict["decl"] = lambda x: x - 1
		self.unary_operation_dict["negl"] = lambda x: -x
		self.unary_operation_dict["notl"] = lambda x: ~x

		self.binary_operation_dict = {}
		self.binary_operation_dict["movl"]  = lambda x, y: y
		self.binary_operation_dict["addl"]  = lambda x, y: x + y
		self.binary_operation_dict["subl"]  = lambda x, y: x - y
		self.binary_operation_dict["imull"] = lambda x, y: x * y
		self.binary_operation_dict["orl"]  = lambda x, y: x | y
		self.binary_operation_dict["andl"] = lambda x, y: x & y
		self.binary_operation_dict["xorl"] = lambda x, y: x ^ y

		self.shift_operation_dict = {}
		self.shift_operation_dict["sarl"] = lambda x, y: x >> y
		self.shift_operation_dict["sall"] = lambda x, y: x << y

		self.register_table = self.segment_register.register_table.copy()
		self.register_table.update(self.integer_register.register_table)
		self.register_table.update(self.special_register.register_table)

	def set_condition_code(self, _ins, _first_source, _second_source):
		self.set_reg(0, "ZF")
		self.set_reg(0, "SF")
		result = None
		if _ins == "cmpl":
			result = _second_source - _first_source
		elif _ins == "testl":
			result = _second_source & _first_source

		assert(result != None)

		if result == 0:
			self.set_reg(1, "ZF")
		elif result < 0:
			self.set_reg(1, "SF")

	def jump_to_label(self, _ins, _label):
		Jump = False
		if _ins == "jmp":
			Jump = True
		elif _ins == "jge" and (self.get_reg("ZF") == 1 or self.get_reg("SF") == 0):
			Jump = True
		elif _ins in ["je", "jne", "js", "jns", "jg", "jl", "jle"]:
			print("***\nTO BE IMPLEMENTED: {}\n***".format(_ins))
			exit()
		if Jump:
			self.set_reg(self.label_table[_label[1:]], "eip")

	def set_reg(self, _value, _reg):
		try:
			self.register_table[_reg].set_value(_value)
		except LookupError:
			print("***\nRegister not found: [" + _reg + "]\n***")

	def set_reg_value_by_source(self, _ins, _source, _reg):
		self.set_reg(self.binary_operation_dict[_ins](self.get_reg(_reg), _source), _reg)

	def get_reg(self, _reg):
	    try:
	        return self.register_table[_reg].get_value()
	    except LookupError:
	    	print("***\nRegister not found: [" + _reg + "]\n***")

	def init_memory(self, _min, _max):
		self.memory.init(_min, _max)

	def set_memory(self, _value, _address):
		self.memory.set(_value, _address)

	def unary_oeprate_source_reg(self, _unary_ins, _reg):
		self.set_reg(self.unary_operation_dict[_unary_ins](self.get_reg(_reg)), _reg)

	def unary_operate_memory_num(self, _unary_ins, _num):
		address = _num
		self.set_memory(self.unary_operation_dict[_unary_ins](self.get_memory(address)), address)

	def unary_operate_memory_reg(self, _unary_ins, _reg):
		address = self.get_reg(_reg)
		self.set_memory(self.unary_operation_dict[_unary_ins](self.get_memory(address)), address)

	def unary_operate_memory_num_reg(self, _unary_ins, _num, _reg):
		address = _num + self.get_reg(_reg)
		self.set_memory(self.unary_operation_dict[_unary_ins](self.get_memory(address)), address)

	def unary_operate_memory_reg_reg(self, _unary_ins, _first_reg, _second_reg):
		address = self.get_reg(_first_reg) + self.get_reg(_second_reg)
		self.set_memory(self.unary_operation_dict[_unary_ins](self.get_memory(address)), address)

	def unary_operate_memory_num_reg_reg(self, _unary_ins, _num, _first_reg, _second_reg):
		address = _num + self.get_reg(_first_reg) + self.get_reg(_second_reg)
		self.set_memory(self.unary_operation_dict[_unary_ins](self.get_memory(address)), address)

	def unary_operate_memory_reg_scale(self, _unary_ins, _reg, _scale_factor):
		address = self.get_reg(_reg) * _scale_factor
		self.set_memory(self.unary_operation_dict[_unary_ins](self.get_memory(address)), address)

	def unary_operate_memory_num_reg_scale(self, _unary_ins, _num, _reg, _scale_factor):
		address = self.get_reg(_reg) * _scale_factor + _num
		self.set_memory(self.unary_operation_dict[_unary_ins](self.get_memory(address)), address)

	def unary_operate_memory_reg_reg_scale(self, _unary_ins, _first_reg, _second_reg, _scale_factor):
		address = self.get_reg(_first_reg) + self.get_reg(_second_reg) * _scale_factor
		self.set_memory(self.unary_operation_dict[_unary_ins](self.get_memory(address)), address)

	def unary_operate_memory_num_reg_reg_scale(self, _unary_ins, _num, _first_reg, _second_reg, _scale_factor):
		address = _num + self.get_reg(_first_reg) + self.get_reg(_second_reg) * _scale_factor
		self.set_memory(self.unary_operation_dict[_unary_ins](self.get_memory(address)), address)

	def binary_operate_source_reg(self, _binary_ins, _source, _reg):
		address = self.get_reg(_reg)
		self.set_memory(self.binary_operation_dict[_binary_ins](self.get_reg(_reg), _source), address)

	def binary_operate_source_num_reg(self, _binary_ins, _source, _num, _reg):
		address = self.get_reg(_reg)+_num
		self.set_memory(self.binary_operation_dict[_binary_ins](self.get_memory(address), _source), address)

	def binary_operate_source_num(self, _binary_ins, _source, _num):
		address = _num
		self.set_memory(self.binary_operation_dict[_binary_ins](self.get_memory(address), _source), address)

	def binary_operate_source_reg_reg_scale(self, _binary_ins, _source, _first_source_reg, _second_source_reg, _scale_factor):
		address = self.get_reg(_first_source_reg) + self.get_reg(_second_source_reg) * _scale_factor
		self.set_memory(self.binary_operation_dict[_binary_ins](self.get_memory(address), _source), address)

	def get_memory(self, _address):
		return self.memory.get(_address)

	def lea_num_reg(self, _num, _source_reg, _dest_reg):
		self.set_reg(self.get_reg(_source_reg)+_num,_dest_reg)

	def lea_reg_reg(self, _first_source_reg, _second_source_reg, _dest_reg):
		self.set_reg(self.get_reg(_first_source_reg)+self.get_reg(_second_source_reg), _dest_reg)

	def lea_reg_reg_num(self, _first_source_reg, _second_source_reg, _num, _dest_reg):
		self.set_reg(self.get_reg(_first_source_reg)+self.get_reg(_second_source_reg)*_num, _dest_reg)

	def lea_num_reg_reg_scale(self, _num, _first_source_reg, _second_source_reg, _scale_factor, _dest_reg):
		self.set_reg(_num+self.get_reg(_first_source_reg)+self.get_reg(_second_source_reg)*_scale_factor, _dest_reg)

	def lea_num_reg_scale(self, _num, _source_reg, _scale_factor, _dest_reg):
		self.set_reg(_num+self.get_reg(_source_reg)*_scale_factor, _dest_reg)

	def shift_operate(self, _ins, _num, _reg):
		self.set_reg(self.shift_operation_dict[_ins](self.get_reg(_reg), _num), _reg)

	def print_register(self):
		self.integer_register.print_self()
		self.special_register.print_self()
		self.segment_register.print_self()

	def print_memory(self):
		self.memory.print_self()

	def print_self(self):
		self.print_register()
		print("LABEL TABLE")
		print(self.label_table)
		print()
		self.print_memory()
