def fact_for(n):
	result = 1
	for i in range(2, n+1):
		result *= i
	return result

for i in range(1, 10):
	print("fact_for({}) = {}".format(i, fact_for(i)))