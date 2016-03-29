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
	parser.add_argument("AsmFile", type=str, help="Assembly File")
	parser.add_argument("min", type=int, help="Memory allocate from")
	parser.add_argument("max", type=int, help="Memory allocate to")
	args = parser.parse_args()

	MySim = Simulator()
	MySim.initMemory(args.min, args.max)

	MySim.readFile(args.AsmFile)
	R86Processor.printSelf()

