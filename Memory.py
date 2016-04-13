class Memory:
	def __init__(self):
		self.name = "MEMORY"
		self.content = {}

	def init(self, _min, _max):
		self.address_min = _min
		self.address_max = _max

		for i in range(int(self.address_min/4), int(self.address_max/4)+1):
			self.content[i*4] = 0

	def set(self, _val, _address):
		if _address > self.address_max or _address < self.address_min or _address%4 != 0:
			print("Illegal access to memory: {}".format(_address))
			exit()
		self.content[_address] = _val
		if _address > self.address_max:
			self.address_max = _address

	def get(self, _address):
		try:
			return self.content[_address]
		except LookupError:
			print("Illegal access to memory: {}".format(_address))
			exit()

	def print_self(self):
		print(self.name)
		for i in reversed(range(int(self.address_min/4), int(self.address_max/4)+1)):
			print("[" + str(i*4) + "]: " + str(self.get(i*4)))