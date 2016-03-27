class Storage:
	def __init__(self, vCapacity):
		self.Name = "MEMORY"
		self.Content = {}
		self.AddressMin = 0
		self.AddressMax = 0

	def set(self, vVal, vAddress):
		self.Content[vAddress] = vVal
		if vAddress > self.AddressMax:
			self.AddressMax = vAddress

	def get(self, vAddress):
		return self.Content[vAddress]

	def printSelf(self):
		print(self.Name)

		for i in range(int(self.AddressMin/4), int(self.AddressMax/4)+1):
			oppose = int(self.AddressMax/4) - i
			print("[" + str(oppose*4) + "]: " + str(self.Content[oppose*4]))