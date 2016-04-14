def loop_while(a, b):
	result = 1
	while a < b:
		result *= (a+b)
		a += 1
	return result

a = 0
b = 4
print("loop_while({}, {}) = {}".format(a, b, loop_while(a, b)))