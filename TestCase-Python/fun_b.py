def fun_b(x):
	val = 0
	i = 0
	for i in range(0, 32):
		val = (2*val) | (x & 1)
		x >>= 1
		i += 1
	return val

def fun_b_2(x):
	ebx = x
	eax = 0
	ecx = 0
	while True:
		edx = eax + eax
		eax = ebx
		eax &= 1
		eax |= edx
		ebx >>= 1
		ecx = ecx + 1
		if ecx - 32 == 0:
			break
	return eax

for i in range(10):
	print("fun_b({})   = {}".format(i, fun_b(i)))
	#print("fun_b_2({}) = {}".format(i, fun_b_2(i)))