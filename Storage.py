class Storage:
	def __init__(self, vCapacity):
		self.Name = "MEMORY"
		self.Content = {}

	def init(self, vMin, vMax):
		self.AddressMin = vMin
		self.AddressMax = vMax

		for i in range(int(self.AddressMin/4), int(self.AddressMax/4)+1):
			self.Content[i*4] = 0

	def set(self, vVal, vAddress):
		if vAddress > self.AddressMax or vAddress < self.AddressMin or vAddress%4!=0:
			print("Illegal access to memory")
			return
		self.Content[vAddress] = vVal
		if vAddress > self.AddressMax:
			self.AddressMax = vAddress

	def get(self, vAddress):
		try:
			return self.Content[vAddress]
		except LookupError:
			print("Illegal access to memory")

	def printSelf(self):
		print(self.Name)
		for i in reversed(range(int(self.AddressMin/4), int(self.AddressMax/4)+1)):
			print("[" + str(i*4) + "]: " + str(self.get(i*4)))