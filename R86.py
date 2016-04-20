from Register import SegmentRegister, IntegerRegister, SpecialRegister
from Memory   import Memory

class R86:
	def __init__(self):
		self.segment_register = SegmentRegister()
		self.integer_register = IntegerRegister()
		self.special_register = SpecialRegister()
		self.memory = Memory()

		self.code_segment = []
		self.label_table  = {}

		self.unary_operation_dict = {}
		self.unary_operation_dict["incl"] = lambda x: x + 1
		self.unary_operation_dict["decl"] = lambda x: x - 1
		self.unary_operation_dict["negl"] = lambda x: -x
		self.unary_operation_dict["notl"] = lambda x: ~x
		self.unary_operation_dict["shrl"] = lambda x: x >> 1
		self.unary_operation_dict["shll"] = lambda x: x >> 1

		self.binary_operation_dict = {}
		self.binary_operation_dict["addl"]  = lambda x, y: x + y
		self.binary_operation_dict["subl"]  = lambda x, y: x - y
		self.binary_operation_dict["imull"] = lambda x, y: x * y
		self.binary_operation_dict["orl"]  = lambda x, y: x | y
		self.binary_operation_dict["andl"] = lambda x, y: x & y
		self.binary_operation_dict["xorl"] = lambda x, y: x ^ y

		self.binary_operation_dict["shrl"] = lambda x, y: x >> y
		self.binary_operation_dict["shll"] = lambda x, y: x << y

		self.register_table = self.segment_register.register_table.copy()
		self.register_table.update(self.integer_register.register_table)
		self.register_table.update(self.special_register.register_table)

	def unary_operate(self, ins, dest):
		result = self.unary_operation_dict[ins](self.get(dest))
		self.set(result, dest)
		self.set_condition_code(result)

	def binary_operate(self, ins, source, dest):
		result = self.binary_operation_dict[ins](self.get(dest), source)
		self.set(result, dest)
		self.set_condition_code(result)

	def compare(self, ins, second_source, first_source):
		self.set_condition_code(first_source - second_source)

	def test(self, ins, second_source, first_source):
		self.set_condition_code(first_source & second_source)

	def jump_to_table(self, label, offset):
		self.set_reg(self.label_table[label]+offset, "eip")
		target_label_line = self.code_segment[self.get_reg("eip")+1]
		target_label = target_label_line[len(".long"):].strip()
		label_pos = self.label_table[target_label]
		self.set_reg(label_pos, "eip")

		#print("label_pos : {}".format(label_pos))

	def conditional_jump(self, ins, label):
		should_jump = {
			"jmp": True,
			"je" : self.get_reg("ZF"),
			"jne": not self.get_reg("ZF"),
			"jl" : self.get_reg("SF"),
			"jle": self.get_reg("SF") or self.get_reg("ZF"),
			"jg" : not (self.get_reg("SF") or self.get_reg("ZF")),
			"jge": not self.get_reg("SF"),
			"js" : self.get_reg("SF"),
			"jns": not self.get_reg("SF")
		}[ins]

		if should_jump:
			self.set_reg(self.label_table[label], "eip")

	def set_condition_code(self, result):
		if result == 0:
			self.set_reg(1, "ZF")
			self.set_reg(0, "SF")
		elif result < 0:
			self.set_reg(0, "ZF")
			self.set_reg(1, "SF")
		else: #result > 0
			self.set_reg(0, "ZF")
			self.set_reg(0, "SF")

	def set(self, source_value, dest):
		if dest in self.integer_register.name_list:
			self.set_reg(source_value, dest)
		else:
			self.set_memory(source_value, dest)

	def get(self, dest):
		if dest in self.integer_register.name_list:
			return self.get_reg(dest)
		else:
			return self.get_memory(dest)

	def set_reg(self, _value, reg):
		try:
			self.register_table[reg].set_value(_value)
		except LookupError:
			print("***\nRegister not found: [" + reg + "]\n***")
			exit()

	def get_reg(self, reg):
		try:
			return self.register_table[reg].get_value()
		except LookupError:
			print("***\nRegister not found: [" + reg + "]\n***")
			exit()

	def init_memory(self, _min, _max):
		self.memory.init(_min, _max)

	def set_memory(self, _value, _address):
		self.memory.set(_value, _address)

	def get_memory(self, _address):
		return self.memory.get(_address)

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
