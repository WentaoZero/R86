from Parser import yacc
from Parser import R86Processor
import argparse

class Simulator:
	def initMemory(self, vMin, vMax):
		R86Processor.initMemory(vMin, vMax)

	def readFile(self, vFileName):
		with open(vFileName) as InputFile:
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

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("asm", type=str, help="Assembly file")
	parser.add_argument("begin", type=int, help="Memory allocated from")
	parser.add_argument("end", type=int, help="Memory allocated to")
	args = parser.parse_args()

	MySim = Simulator()
	MySim.initMemory(args.begin, args.end)

	MySim.readFile(args.asm)
	R86Processor.printSelf()

