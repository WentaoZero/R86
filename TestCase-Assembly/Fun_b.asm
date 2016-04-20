;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $3, 4(%ebp)
	;set x

;fun_b:
	pushl %ebp
	movl %esp, %ebp

	movl 8(%ebp), %ebx
	movl $0, %eax
	movl $0, %ecx

.L13:
	leal (%eax,%eax), %edx
	movl %ebx, %eax
	andl $1, %eax
	orl %edx, %eax
	shrl %ebx
	addl $1, %ecx
	cmpl $32, %ecx
	jne .L13