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
					if is_label(CleanLine):
						R86Processor.label_table[get_label(CleanLine)] = len(R86Processor.code_segment)
					R86Processor.code_segment.append(CleanLine)

	def startSimulation(self):
		while R86Processor.EIP < len(R86Processor.code_segment):
			#if (R86Processor.code_segment[R86Processor.EIP] == "movl (%eax), %edx"):
			yacc.parse(R86Processor.code_segment[R86Processor.EIP])
			R86Processor.EIP += 1;

	def printSelf(self):
		R86Processor.printSelf()
	def printReg(self):
		R86Processor.printReg()
	def printMemory(self):
		R86Processor.printMemory()

import re

def is_label(line):
	line = drop_comment(drop__space_and_tab(line))
	matchObj = re.match(r"\.(.*):", line)
	if matchObj:
		return True
	else:
		return False

def get_label(line):
	line = drop_comment(drop__space_and_tab(line))
	matchObj = re.match(r"\.(.*):", line)
	return matchObj.group(1)

def drop__space_and_tab(line):
	new_line = str()
	for item in line:
		if item not in [" ", "\t"]:
			new_line += item
	return new_line

def drop_comment(line):
	num = line.find(";")
	if num != -1:
		return line[:num]
	else:
		return line

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("asm",   type=str, help="Assembly file")
	parser.add_argument("begin", type=int, help="Memory allocated from")
	parser.add_argument("end",   type=int, help="Memory allocated to")
	args = parser.parse_args()

	MySim = Simulator()
	MySim.initMemory(args.begin, args.end)

	MySim.readFile(args.asm)
	MySim.startSimulation()

	#print(R86Processor.label_table)

	R86Processor.printSelf()

	print
