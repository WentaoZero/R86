;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $4, 4(%ebp)
	;set x

;fun_a:
	pushl %ebp
	movl %esp, %ebp

	movl 8(%ebp), %edx
	movl $0, %eax
	testl %edx, %edx
	je .L7

.L10:
	xorl %edx, %eax
	sarl %edx
	jne .L10

.L7:
	andl $1, %eax