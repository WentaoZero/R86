def fun_a(x):
	val = 0
	while x != 0:
		val = val ^ x
		x = x >> 1
	return val & 1

for i in range(10):
	print("fun_a({}) = {}".format(i, fun_a(i)))