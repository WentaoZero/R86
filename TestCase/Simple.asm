;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $36, %eax
	;set xp
	movl $-3, (%eax)
	movl %eax, 4(%ebp)
	;set *xp
	movl %ebp, (%ebp)
	;store %ebp
	movl $20, 8(%ebp)
	;set y

;Simple:
	pushl %ebp
	movl %esp, %ebp

	movl 8(%ebp), %edx
	movl 12(%ebp), %eax
	addl (%edx), %eax
	movl %eax, (%edx)

	popl %ebp