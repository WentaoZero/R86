import re
from Parser import yacc
from Parser import R86Processor

class Simulator:
	def init_memory(self, min, max):
		R86Processor.init_memory(min, max)

	def readFile(self, file_name):
		with open(file_name) as input_file:
			for line in input_file:
				cleaned_line = line.strip("\n\t")
				if (0 != len(cleaned_line) and cleaned_line[0] != ";"):
					label = get_label(cleaned_line)
					if label:
						R86Processor.label_table[label] = len(R86Processor.code_segment)
					R86Processor.code_segment.append(cleaned_line)

	def startSimulation(self):
		while R86Processor.get_reg("eip") < len(R86Processor.code_segment):
			yacc.parse(R86Processor.code_segment[R86Processor.get_reg("eip")])
			R86Processor.set_reg(R86Processor.get_reg("eip")+1, "eip")
	def print_self(self):
		R86Processor.print_self()
	def printReg(self):
		R86Processor.printReg()
	def printMemory(self):
		R86Processor.printMemory()

def get_label(line):
	line = line.strip("\t ")
	matchObj = re.match(r"(\.[a-zA-Z]+[a-zA-Z0-9]*):", line)
	if matchObj:
		return matchObj.group(1)

if __name__ == "__main__":

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument("asm",   type=str, help="Assembly file")
	parser.add_argument("begin", type=int, help="Memory allocated from")
	parser.add_argument("end",   type=int, help="Memory allocated to")
	args = parser.parse_args()

	MySim = Simulator()
	MySim.init_memory(args.begin, args.end)

	MySim.readFile(args.asm)
	MySim.startSimulation()

	R86Processor.print_self()