;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16

	movl $0, %eax
	movl $0, %edx

;compare:
	cmpl %eax, %edx
	;testl %eax, %edx

	popl %ebp