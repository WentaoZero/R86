;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $7, 4(%ebp)
	;set x to 11
	movl $19, 8(%ebp)
	;set y to 14
	movl $37, 12(%ebp)
	;set z to 17

;Arith:
	pushl %ebp
	movl %esp, %ebp

	movl 12(%ebp), %eax
	xorl 8(%ebp), %eax
	sarl $3, %eax
	notl %eax
	subl 16(%ebp), %eax

	popl %ebp