;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $7, 4(%ebp)
	;set x
	movl $19, 8(%ebp)
	;set y
	movl $37, 12(%ebp)
	;set z

;Arith:
	pushl %ebp
	movl %esp, %ebp

	movl 12(%ebp), %eax
	xorl 8(%ebp), %eax
	shrl $3, %eax
	notl %eax
	subl 16(%ebp), %eax

	popl %ebp