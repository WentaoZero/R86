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
		self.Content[vAddress] = vVal
		if vAddress > self.AddressMax:
			self.AddressMax = vAddress

	def get(self, vAddress):
		return self.Content[vAddress]

	def printSelf(self):
		print(self.Name)
		for i in reversed(range(int(self.AddressMin/4), int(self.AddressMax/4)+1)):
			print("[" + str(i*4) + "]: " + str(self.Content[i*4]))