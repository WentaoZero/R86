def fact_while(n):
	result = 1
	while n > 1:
		result *= n
		n = n - 1
	return result

n = 6
print("fact({}) = {}".format(n, fact_while(n)))