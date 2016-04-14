;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $19, 4(%ebp)
	;set x
	movl $23, 8(%ebp)
	;set y

;Sum:
	pushl %ebp
	movl %esp, %ebp

	movl 0xc(%ebp), %eax
	addl 0x8(%ebp), %eax

	popl %ebp