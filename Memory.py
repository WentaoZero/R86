class Memory:
	def __init__(self):
		self.name = "MEMORY"
		self.content = {}

	def init(self, min, max):
		self.address_min = min
		self.address_max = max

		for i in range(int(self.address_min/4), int(self.address_max/4)+1):
			self.content[i*4] = 0

	def set(self, val, address):
		if address > self.address_max or address < self.address_min or address%4 != 0:
			print("Illegal access to memory: {}".format(address))
			exit()
		self.content[address] = val
		if address > self.address_max:
			self.address_max = address

	def get(self, address):
		try:
			return self.content[address]
		except LookupError:
			print("Illegal access to memory: {}".format(address))
			exit()

	def print_self(self):
		print(self.name)
		for i in reversed(range(int(self.address_min/4), int(self.address_max/4)+1)):
			print("[" + str(i*4) + "]: " + str(self.get(i*4)))