def dw_loop(x, y, n):
	while(True):
		x += n
		y *= n
		n -= 1
		if not(n > 0 and y < n):
			break
	print("y = {}".format(y))
	return x

print("x = {}".format(dw_loop(0, 0, 7)))