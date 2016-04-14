;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $0, 4(%ebp)
	;set a
	movl $4, 8(%ebp)
	;set b

;Loop_while:
	pushl %ebp
	movl %esp, %ebp

	movl 8(%ebp), %ecx
	movl 12(%ebp), %ebx
	movl $1, %eax
	cmpl %ebx, %ecx
	jge .L11
	leal (%ebx, %ecx), %edx
	movl $1, %eax
	;this statement seems redundant

.L12:
	imull %edx, %eax
	addl $1, %ecx
	addl $1, %edx
	cmpl %ecx, %ebx
	jg .L12

.L11: