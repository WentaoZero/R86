from Register import SegmentRegister, IntegerRegister, SpecialRegister
from Storage  import Storage

class R86:
	def __init__(self):
		self.SegmentReg = SegmentRegister()
		self.IntegerReg = IntegerRegister()
		self.SpecialReg = SpecialRegister()
		self.Memory = Storage(0)

		self.UnaryOperationDict = {}
		self.UnaryOperationDict["incl"] = lambda x: x + 1
		self.UnaryOperationDict["decl"] = lambda x: x - 1
		self.UnaryOperationDict["negl"] = lambda x: -x
		self.UnaryOperationDict["notl"] = lambda x: ~x

		self.BinaryOperationDict = {}
		self.BinaryOperationDict["movl"] = lambda x, y: y
		self.BinaryOperationDict["addl"] = lambda x, y: x + y
		self.BinaryOperationDict["subl"] = lambda x, y: x - y
		self.BinaryOperationDict["imul"] = lambda x, y: x * y
		self.BinaryOperationDict["xorl"] = lambda x, y: x ^ y
		self.BinaryOperationDict["orl"]  = lambda x, y: x | y
		self.BinaryOperationDict["andl"] = lambda x, y: x & y

		self.ShiftOperationDict = {}
		self.ShiftOperationDict["sarl"] = lambda x, y: x >> y
		self.ShiftOperationDict["sall"] = lambda x, y: x << y

		self.RegisterTable = self.SegmentReg.RegisterTable.copy()
		self.RegisterTable.update(self.IntegerReg.RegisterTable)
		self.RegisterTable.update(self.SpecialReg.RegisterTable)

	#do be deleted

	def setReg(self, vValue, vReg):
		try:
			self.RegisterTable[vReg].setValue(vValue)
		except LookupError:
			print("***\nRegister not found: [" + vReg + "]\n***")

	def setRegValueBySource(self, vIns, vSource, vReg):
		self.setReg(self.BinaryOperationDict[vIns](self.getRegValue(vReg), vSource), vReg)

	def getRegValue(self, vReg):
	    try:
	        return self.RegisterTable[vReg].getValue()
	    except LookupError:
	    	print("***\nRegister not found: [" + vReg + "]\n***")

	def initMemory(self, vMin, vMax):
		self.Memory.init(vMin, vMax)

	def setMemory(self, vValue, vAddress):
		self.Memory.set(vValue, vAddress)

	def setMemoryByReg(self, vBinaryIns, vSource, vReg):
		TempAddress = self.getRegValue(vReg)
		self.setMemory(self.BinaryOperationDict[vBinaryIns](self.getRegValue(vReg), vSource), TempAddress)

	def setMemoryByNumberReg(self, vBinaryIns, vSource, vNum, vReg):
		TempAddress = self.getRegValue(vReg)+vNum
		self.setMemory(self.BinaryOperationDict[vBinaryIns](self.getMemory(TempAddress), vSource), TempAddress)

	def setMemoryByNumber(self, vBinaryIns, vSource, vNum):
		TempAddress = vNum
		self.setMemory(self.BinaryOperationDict[vBinaryIns](self.getMemory(TempAddress), vSource), TempAddress)

	def getMemory(self, vAddress):
		return self.Memory.get(vAddress)

	def unaryOperate(self, vUnaryIns, vReg):
		self.setReg(self.UnaryOperationDict[vUnaryIns](self.getRegValue(vReg)), vReg)

	def shiftOperate(self, vIns, vNum, vReg):
		self.setReg(self.ShiftOperationDict[vIns](self.getRegValue(vReg), vNum), vReg)

	def printReg(self):
		self.SegmentReg.printSelf()
		self.IntegerReg.printSelf()
		self.SpecialReg.printSelf()

	def printMemory(self):
		self.Memory.printSelf()

	def printSelf(self):
		self.printReg()
		self.printMemory()
