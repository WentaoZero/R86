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

		self.binary_operate = {}
		self.binary_operate["addl"]  = lambda x, y: x + y
		self.binary_operate["subl"]  = lambda x, y: x - y
		self.binary_operate["imull"] = lambda x, y: x * y
		self.binary_operate["orl"]  = lambda x, y: x | y
		self.binary_operate["andl"] = lambda x, y: x & y
		self.binary_operate["xorl"] = lambda x, y: x ^ y

		self.shift_operation_dict = {}
		self.shift_operation_dict["sarl"] = lambda x, y: x >> y
		self.shift_operation_dict["sall"] = lambda x, y: x << y

		self.register_table = self.segment_register.register_table.copy()
		self.register_table.update(self.integer_register.register_table)
		self.register_table.update(self.special_register.register_table)

	def set_condition_code(self, _result):
		if _result == 0:
			self.set_reg(1, "ZF")
			self.set_reg(0, "SF")
		elif _result < 0:
			self.set_reg(0, "ZF")
			self.set_reg(1, "SF")
		else: # result > 0
			self.set_reg(0, "ZF")
			self.set_reg(0, "SF")

	def jump_to_label(self, ins, label):
		Jump = False
		if ins == "jmp":
			Jump = True
		elif ins == "jge":
			Jump = self.get_reg("ZF") or (not self.get_reg("SF"))
		elif ins == "je":
			Jump = self.get_reg("ZF")
		elif ins == "jne":
			Jump = self.get_reg("ZF")
		elif ins == "js":
			Jump = self.get_reg("SF")
		elif ins == "jns":
			Jump = not self.get_reg("SF")
		elif ins == "jg":
			Jump = (not self.get_reg("SF")) and (not self.get_reg("ZF"))
		elif ins == "jl":
			Jump = self.get_reg("SF")
		elif ins == "jle":
			Jump = self.get_reg("SF") or self.get_reg("ZF")
		if Jump:
			self.set_reg(self.label_table[label[1:]], "eip")

	def set(self, source_value, dest):
		if dest in ["eax","ecx","edx","ebx","esi","edi","esp","ebp"]:
			self.set_reg(source_value, dest)
		else:
			self.set_memory(source_value, dest)

	def get(self, dest):
		if dest in ["eax","ecx","edx","ebx","esi","edi","esp","ebp"]:
			return self.get_reg(dest)
		else:
			return self.get_memory(dest)

	def set_reg(self, _value, reg):
		try:
			self.register_table[reg].set_value(_value)
		except LookupError:
			print("***\nRegister not found: [" + reg + "]\n***")
			exit()

	def set_reg_value_by_source(self, ins, source, reg):
		self.set_reg(self.binary_operate[ins](self.get_reg(reg), source), reg)

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

	def unary_oeprate_source_reg(self, unaryins, reg):
		self.set_reg(self.unary_operation_dict[unaryins](self.get_reg(reg)), reg)

	def unary_operate_memory_num(self, unaryins, num):
		address = num
		self.set_memory(self.unary_operation_dict[unaryins](self.get_memory(address)), address)

	def unary_operate_memory_reg(self, unaryins, reg):
		address = self.get_reg(reg)
		self.set_memory(self.unary_operation_dict[unaryins](self.get_memory(address)), address)

	def unary_operate_memory_num_reg(self, unaryins, num, reg):
		address = num + self.get_reg(reg)
		self.set_memory(self.unary_operation_dict[unaryins](self.get_memory(address)), address)

	def unary_operate_memory_reg_reg(self, unaryins, first_reg, second_reg):
		address = self.get_reg(first_reg) + self.get_reg(second_reg)
		self.set_memory(self.unary_operation_dict[unaryins](self.get_memory(address)), address)

	def unary_operate_memory_num_reg_reg(self, unaryins, num, first_reg, second_reg):
		address = num + self.get_reg(first_reg) + self.get_reg(second_reg)
		self.set_memory(self.unary_operation_dict[unaryins](self.get_memory(address)), address)

	def unary_operate_memory_reg_scale(self, unaryins, reg, _scale_factor):
		address = self.get_reg(reg) * _scale_factor
		self.set_memory(self.unary_operation_dict[unaryins](self.get_memory(address)), address)

	def unary_operate_memory_num_reg_scale(self, unaryins, num, reg, _scale_factor):
		address = self.get_reg(reg) * _scale_factor + num
		self.set_memory(self.unary_operation_dict[unaryins](self.get_memory(address)), address)

	def unary_operate_memory_reg_reg_scale(self, unaryins, first_reg, second_reg, _scale_factor):
		address = self.get_reg(first_reg) + self.get_reg(second_reg) * _scale_factor
		self.set_memory(self.unary_operation_dict[unaryins](self.get_memory(address)), address)

	def unary_operate_memory_num_reg_reg_scale(self, unaryins, num, first_reg, second_reg, _scale_factor):
		address = num + self.get_reg(first_reg) + self.get_reg(second_reg) * _scale_factor
		self.set_memory(self.unary_operation_dict[unaryins](self.get_memory(address)), address)

	def lea_num_reg(self, num, _source_reg, dest_reg):
		self.set_reg(self.get_reg(_source_reg)+num,dest_reg)

	def lea_reg_reg(self, first_source_reg, second_source_reg, dest_reg):
		self.set_reg(self.get_reg(first_source_reg)+self.get_reg(second_source_reg), dest_reg)

	def lea_reg_reg_num(self, first_source_reg, second_source_reg, num, dest_reg):
		self.set_reg(self.get_reg(first_source_reg)+self.get_reg(second_source_reg)*num, dest_reg)

	def lea_num_reg_reg_scale(self, num, first_source_reg, second_source_reg, _scale_factor, dest_reg):
		self.set_reg(num+self.get_reg(first_source_reg)+self.get_reg(second_source_reg)*_scale_factor, dest_reg)

	def lea_num_reg_scale(self, num, _source_reg, _scale_factor, dest_reg):
		self.set_reg(num+self.get_reg(_source_reg)*_scale_factor, dest_reg)

	def shift_operate(self, ins, num, reg):
		self.set_reg(self.shift_operation_dict[ins](self.get_reg(reg), num), reg)

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
