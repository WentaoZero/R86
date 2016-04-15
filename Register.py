class AtomRegister:
	def __init__(self, name):
		self.name  = name
		self.value = 0

	def get_name(self):
		return self.name

	def set_value(self, value):
		self.value = value

	def get_value(self):
		return self.value

	def print_self(self):
		print(self.name + " = " + str(self.value))

class RegisterBaseV(object):
	def collect_sub_register(self):
		reg_table = dict()
		for reg in self.register_list:
			reg_table[reg.get_name()] = reg
		return reg_table

	def print_self(self):
		print(self.name)
		for reg in self.register_list:
			reg.print_self()
		print("")

class SegmentRegister(RegisterBaseV):
	def __init__(self):
		self.name = "SEGMENT REGISTER"
		self.code_segment  = AtomRegister("cs")
		self.stack_segment = AtomRegister("ss")
		self.data_segment  = AtomRegister("ds")
		self.register_list  = [self.code_segment, self.stack_segment, self.data_segment]
		self.register_table = super(SegmentRegister, self).collect_sub_register()

	def print_self(self):
		super(SegmentRegister, self).print_self()

class IntegerRegister(RegisterBaseV):
	def __init__(self):
		self.name = "INTEGER REGISTER"
		self.EAX = AtomRegister("eax")
		self.ECX = AtomRegister("ecx")
		self.EDX = AtomRegister("edx")
		self.EBX = AtomRegister("ebx")
		self.ESI = AtomRegister("esi")
		self.EDI = AtomRegister("edi")
		self.ESP = AtomRegister("esp")
		self.EBP = AtomRegister("ebp")
		self.register_list  = [self.EAX, self.ECX, self.EDX, self.EBX, self.ESI, self.EDI, self.ESP, self.EBP]
		self.register_table = super(IntegerRegister, self).collect_sub_register()

	def print_self(self):
		super(IntegerRegister, self).print_self()

class EFLAGS(RegisterBaseV):
	def __init__(self):
		self.name = "EXTENDED FLAG REGISTER"
		self.zero_flag   = AtomRegister("ZF")
		self.symbol_flag = AtomRegister("SF")
		self.register_list  = [self.zero_flag, self.symbol_flag]
		self.register_table = super(EFLAGS, self).collect_sub_register()

	def print_self(self):
		super(EFLAGS, self).print_self()

class SpecialRegister(RegisterBaseV):
	def __init__(self):
		self.name = "SPECIAL REGISTER"
		self.EIP = AtomRegister("eip")
		self.flags_register = EFLAGS()
		self.register_list  = [self.EIP] + self.flags_register.register_list

		self.register_table = super(SpecialRegister, self).collect_sub_register()

	def print_self(self):
		super(SpecialRegister, self).print_self()
