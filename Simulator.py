from Parser import yacc
from Parser import R86Processor

class Simulator:
	def setMemory(self):
		for i in range(0, 10):
			R86Processor.setMemory(0, i*4)
	def readFile(self):
		with open("Simple.asm") as InputFile:
			for line in InputFile:
				CleanLine = line.strip("\n\t")
				if (0 != len(CleanLine) and CleanLine[0] != ";"):
					yacc.parse(CleanLine)
	def printSelf(self):
		R86Processor.printSelf()
	def printReg(self):
		R86Processor.printReg()
	def printMemory(self):
		R86Processor.printMemory()

MySim = Simulator()
MySim.setMemory()
MySim.readFile()
R86Processor.printSelf()