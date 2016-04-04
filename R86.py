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
		self.BinaryOperationDict["imull"] = lambda x, y: x * y
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
		self.setReg(self.BinaryOperationDict[vIns](self.getReg(vReg), vSource), vReg)

	def getReg(self, vReg):
	    try:
	        return self.RegisterTable[vReg].getValue()
	    except LookupError:
	    	print("***\nRegister not found: [" + vReg + "]\n***")

	def initMemory(self, vMin, vMax):
		self.Memory.init(vMin, vMax)

	def setMemory(self, vValue, vAddress):
		self.Memory.set(vValue, vAddress)

	def unary_oeprate_source_reg(self, vUnaryIns, vReg):
		self.setReg(self.UnaryOperationDict[vUnaryIns](self.getReg(vReg)), vReg)

	def unary_operate_memory_num(self, vUnaryIns, vNum):
		TempAddress = vNum
		self.setMemory(self.UnaryOperationDict[vUnaryIns](self.getMemory(TempAddress)), TempAddress)

	def unary_operate_memory_reg(self, vUnaryIns, vReg):
		TempAddress = self.getReg(vReg)
		self.setMemory(self.UnaryOperationDict[vUnaryIns](self.getMemory(TempAddress)), TempAddress)

	def unary_operate_memory_num_reg(self, vUnaryIns, vNum, vReg):
		TempAddress = vNum + self.getReg(vReg)
		self.setMemory(self.UnaryOperationDict[vUnaryIns](self.getMemory(TempAddress)), TempAddress)

	def unary_operate_memory_reg_reg(self, vUnaryIns, vFirstReg, vSecondReg):
		TempAddress = self.getReg(vFirstReg) + self.getReg(vSecondReg)
		self.setMemory(self.UnaryOperationDict[vUnaryIns](self.getMemory(TempAddress)), TempAddress)

	def unary_operate_memory_num_reg_reg(self, vUnaryIns, vNum, vFirstReg, vSecondReg):
		TempAddress = vNum + self.getReg(vFirstReg) + self.getReg(vSecondReg)
		self.setMemory(self.UnaryOperationDict[vUnaryIns](self.getMemory(TempAddress)), TempAddress)

	def unary_operate_memory_reg_scale(self, vUnaryIns, vReg, vScaleFactor):
		TempAddress = self.getReg(vReg) * vScaleFactor
		self.setMemory(self.UnaryOperationDict[vUnaryIns](self.getMemory(TempAddress)), TempAddress)

	def unary_operate_memory_num_reg_scale(self, vUnaryIns, vNum, vReg, vScaleFactor):
		TempAddress = self.getReg(vReg) * vScaleFactor + vNum
		self.setMemory(self.UnaryOperationDict[vUnaryIns](self.getMemory(TempAddress)), TempAddress)

	def unary_operate_memory_reg_reg_scale(self, vUnaryIns, vFirstReg, vSecondReg, vScaleFactor):
		TempAddress = self.getReg(vFirstReg) + self.getReg(vSecondReg) * vScaleFactor
		self.setMemory(self.UnaryOperationDict[vUnaryIns](self.getMemory(TempAddress)), TempAddress)

	def unary_operate_memory_num_reg_reg_scale(self, vUnaryIns, vNum, vFirstReg, vSecondReg, vScaleFactor):
		TempAddress = vNum + self.getReg(vFirstReg) + self.getReg(vSecondReg) * vScaleFactor
		self.setMemory(self.UnaryOperationDict[vUnaryIns](self.getMemory(TempAddress)), TempAddress)

	def binary_operate_source_reg(self, vBinaryIns, vSource, vReg):
		TempAddress = self.getReg(vReg)
		self.setMemory(self.BinaryOperationDict[vBinaryIns](self.getReg(vReg), vSource), TempAddress)

	def binary_operate_source_num_reg(self, vBinaryIns, vSource, vNum, vReg):
		TempAddress = self.getReg(vReg)+vNum
		self.setMemory(self.BinaryOperationDict[vBinaryIns](self.getMemory(TempAddress), vSource), TempAddress)

	def binary_operate_source_num(self, vBinaryIns, vSource, vNum):
		TempAddress = vNum
		self.setMemory(self.BinaryOperationDict[vBinaryIns](self.getMemory(TempAddress), vSource), TempAddress)

	def binary_operate_source_reg_reg_scale(self, vBinaryIns, vSource, vFirstSourceReg, vSecondSourceReg, vScaleFactor):
		TempAddress = self.getReg(vFirstSourceReg) + self.getReg(vSecondSourceReg) * vScaleFactor
		self.setMemory(self.BinaryOperationDict[vBinaryIns](self.getMemory(TempAddress), vSource), TempAddress)

	def getMemory(self, vAddress):
		return self.Memory.get(vAddress)

	def leaNumReg(self, vNum, vSourceReg, vDestReg):
		self.setReg(self.getReg(vSourceReg)+vNum,vDestReg)

	def leaRegReg(self, vFirstSourceReg, vSecondSourceReg, vDestReg):
		self.setReg(self.getReg(vFirstSourceReg)+self.getReg(vSecondSourceReg), vDestReg)

	def leaRegRegNum(self, vFirstSourceReg, vSecondSourceReg, vNum, vDestReg):
		self.setReg(self.getReg(vFirstSourceReg)+self.getReg(vSecondSourceReg)*vNum, vDestReg)

	def leaNumRegRegScale(self, vNum, vFirstSourceReg, vSecondSourceReg, vScaleFactor, vDestReg):
		self.setReg(vNum+self.getReg(vFirstSourceReg)+self.getReg(vSecondSourceReg)*vScaleFactor, vDestReg)

	def leaNumRegScale(self, vNum, vSourceReg, vScale, vDestReg):
		self.setReg(vNum+self.getReg(vSourceReg)*vScale, vDestReg)

	def shiftOperate(self, vIns, vNum, vReg):
		self.setReg(self.ShiftOperationDict[vIns](self.getReg(vReg), vNum), vReg)

	def printReg(self):
		self.SegmentReg.printSelf()
		self.IntegerReg.printSelf()
		self.SpecialReg.printSelf()

	def printMemory(self):
		self.Memory.printSelf()

	def printSelf(self):
		self.printReg()
		self.printMemory()
