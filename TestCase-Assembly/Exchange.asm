;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $20, %eax
	;set xp to 20
	movl $9, (%eax)
	movl %eax, 4(%ebp)
	;set *xp to 9
	movl %ebp, (%ebp)
	;store %ebp
	movl $8, 8(%ebp)
	;set y to 8

;Exchange:
	pushl %ebp
	movl %esp, %ebp

	movl 8(%ebp), %edx
	movl (%edx), %eax
	movl 12(%ebp), %ecx
	movl %ecx, (%edx)

	popl %ebp