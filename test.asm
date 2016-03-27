;prepare
	movl $-3, 36
	movl $16, %ebp
	movl %ebp, %esp
	movl $36, 4(%ebp)
	movl %ebp, (%ebp)
	movl $20, 8(%ebp)
	movl $36, 4(%ebp)

	pushl %ebp
	movl %esp, %ebp
	movl 8(%ebp), %edx
	movl 12(%ebp), %eax
	addl (%edx), %eax
	movl %eax, (%edx)
	popl %ebp