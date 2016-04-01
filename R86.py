from Register import SegmentRegister, IntegerRegister, SpecialRegister
from Storage  import Storage

class R86:
	def __init__(self):
		self.SegmentReg = SegmentRegister()
		self.IntegerReg = IntegerRegister()
		self.SpecialReg = SpecialRegister()
		self.Memory = Storage(0)

		self.SingleArithDict = {}
		self.SingleArithDict["incl"] = lambda x: x + 1
		self.SingleArithDict["decl"] = lambda x: x - 1
		self.SingleArithDict["negl"] = lambda x: -x
		self.SingleArithDict["notl"] = lambda x: ~x

		self.DoubleArithDict = {}
		self.DoubleArithDict["addl"] = lambda x, y: x + y
		self.DoubleArithDict["subl"] = lambda x, y: x - y
		self.DoubleArithDict["imul"] = lambda x, y: x * y
		self.DoubleArithDict["xorl"] = lambda x, y: x ^ y
		self.DoubleArithDict["orl"]  = lambda x, y: x | y
		self.DoubleArithDict["andl"] = lambda x, y: x & y

		self.shiftDict = {}
		self.shiftDict["sarl"] = lambda x, y: x >> y
		self.shiftDict["sall"] = lambda x, y: x << y

		self.RegisterTable = self.SegmentReg.RegisterTable.copy()
		self.RegisterTable.update(self.IntegerReg.RegisterTable)
		self.RegisterTable.update(self.SpecialReg.RegisterTable)

	def setRegValue(self, vValue, vReg):
	    try:
	        self.RegisterTable[vReg].setValue(vValue)
	    except LookupError:
	        print("***\nRegister not found: [" + vReg + "]\n***")

	def getRegValue(self, vReg):
	    try:
	        return self.RegisterTable[vReg].getValue()
	    except LookupError:
	    	print("***\nRegister not found: [" + vReg + "]\n***")

	def initMemory(self, vMin, vMax):
		self.Memory.init(vMin, vMax)

	def setMemory(self, vValue, vAddress):
		self.Memory.set(vValue, vAddress)

	def getMemory(self, vAddress):
		return self.Memory.get(vAddress)

	def singleArithOperate(self, vIns, vReg):
		self.setRegValue(self.SingleArithDict[vIns](self.getRegValue(vReg)), vReg)

	def doubleArithOperate(self, vIns, vSource, vReg):
		self.setRegValue(self.DoubleArithDict[vIns](self.getRegValue(vReg), vSource), vReg)

	def shiftOperate(self, vIns, vNum, vReg):
		self.setRegValue(self.shiftDict[vIns](self.getRegValue(vReg), vNum), vReg)

	def printReg(self):
		self.SegmentReg.printSelf()
		self.IntegerReg.printSelf()
		self.SpecialReg.printSelf()

	def printMemory(self):
		self.Memory.printSelf()

	def printSelf(self):
		self.printReg()
		self.printMemory()
