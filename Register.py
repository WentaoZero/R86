class AtomRegister:
	def __init__(self, vName, vValue=0):
		self.Name  = vName
		self.Value = vValue

	def getName(self):
		return self.Name

	def setValue(self, vValue):
		self.Value = vValue

	def getValue(self):
		return self.Value

	def printSelf(self):
		print("%" + self.Name + " = " + str(self.Value))

class RegisterBaseV(object):
	def collectSubRegister(self):
		RegTable = dict()
		for reg in self.RegisterList:
			RegTable[reg.getName()] = reg
		return RegTable

	def printSelf(self):
		print(self.Name)
		for reg in self.RegisterList:
			reg.printSelf()
		print("")

class SegmentRegister(RegisterBaseV):
	def __init__(self):
		self.Name = "SEGMENT REGISTER"
		self.CS = AtomRegister("cs")
		self.SS = AtomRegister("ss")
		self.DS = AtomRegister("ds")
		self.RegisterList  = [self.CS, self.SS, self.DS]
		self.RegisterTable = super(SegmentRegister, self).collectSubRegister()

	def printSelf(self):
		super(SegmentRegister, self).printSelf()

class IntegerRegister(RegisterBaseV):
	def __init__(self):
		self.Name = "INTEGER REGISTER"
		self.EAX = AtomRegister("eax")
		self.ECX = AtomRegister("ecx")
		self.EDX = AtomRegister("edx")
		self.EBX = AtomRegister("ebx")
		self.ESI = AtomRegister("esi")
		self.EDI = AtomRegister("edi")
		self.ESP = AtomRegister("esp")
		self.EBP = AtomRegister("ebp")
		self.RegisterList  = [self.EAX, self.ECX, self.EDX, self.EBX, self.ESI, self.EDI, self.ESP, self.EBP]
		self.RegisterTable = super(IntegerRegister, self).collectSubRegister()

	def printSelf(self):
		super(IntegerRegister, self).printSelf()

class EFLAGS(RegisterBaseV):
	def __init__(self):
		self.Name = "EXTENDED FLAG REGISTER"
		self.Zero   = AtomRegister("z")
		self.Symbol = AtomRegister("o")
		self.RegisterList  = [self.Zero, self.Symbol]
		self.RegisterTable = super(EFLAGS, self).collectSubRegister()

	def printSelf(self):
		super(EFLAGS, self).printSelf()

class SpecialRegister(RegisterBaseV):
	def __init__(self):
		self.Name = "SPECIAL REGISTER"
		self.EIP = AtomRegister("eip")
		self.FlagsReg = EFLAGS()
		self.RegisterList  = [self.EIP] + self.FlagsReg.RegisterList

		self.RegisterTable = super(SpecialRegister, self).collectSubRegister()

	def printSelf(self):
		super(SpecialRegister, self).printSelf()
