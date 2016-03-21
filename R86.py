from Register import SegmentRegister, IntegerRegister, SpecialRegister
from Storage  import Storage

class R86:
	def __init__(self):
		self.SegmentReg = SegmentRegister()
		self.IntegerReg = IntegerRegister()
		self.SpecialReg = SpecialRegister()
		self.Memory = Storage(5)

		self.RegisterTable = self.SegmentReg.RegisterTable.copy()
		self.RegisterTable.update(self.IntegerReg.RegisterTable)
		self.RegisterTable.update(self.SpecialReg.RegisterTable)

	def setRegValue(self, vReg, vValue):
	    try:
	        self.RegisterTable[vReg].setValue(vValue)
	    except LookupError:
	        print("***\nRegister not found: [" + vReg + "]\n***")

	def getRegValue(self, vReg):
	    try:
	        return self.RegisterTable[vReg].getValue()
	    except LookupError:
	    	print("***\nRegister not found: [" + vReg + "]\n***")

	def setMemory(self, vValue, vAddress):
		self.Memory.set(vValue, vAddress)

	def getMemory(self, vAddress):
		return self.Memory.get(vAddress)

	def printReg(self):
		self.SegmentReg.printSelf()
		self.IntegerReg.printSelf()
		self.SpecialReg.printSelf()

	def printMemory(self):
		self.Memory.printSelf()

	def printSelf(self):
		self.printReg()
		self.printMemory()
