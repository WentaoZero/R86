from Parser import yacc
from Parser import R86Processor
import argparse


class Simulator:
	def setMemory(self):
		for i in range(0, 10):
			R86Processor.setMemory(0, i*4)
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
	args = parser.parse_args()

	MySim = Simulator()
	MySim.setMemory()

	MySim.readFile(args.AsmFile)
	R86Processor.printSelf()

