class Storage:
	def __init__(self, vCapacity):
		self.Name = "MEMORY"
		self.Content = [-1] * vCapacity
		#self.Content = [[0] * vWordLength] * vCapacity

	def set(self, vVal, vAddress):
		self.Content[vAddress] = vVal

	def get(self, vAddress):
		return self.Content[vAddress]

	def printSelf(self):
		print(self.Name)
		count = 0
		for item in self.Content:
			print(str(count) + " " + str(item))
			count += 1
		print("")