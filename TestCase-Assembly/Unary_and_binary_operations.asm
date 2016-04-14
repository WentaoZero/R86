;prepare
	movl $300, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 0x90
	movl $0x100, %eax
	movl $0x1, %ecx
	movl $0x3, %edx
	;register

	movl $0xFF, 0x100
	movl $0xAB, 0x104
	movl $0x13, 0x108
	movl $0x11, 0x10C

;UnaryAndBinaryOperations:
	pushl %ebp
	movl %esp, %ebp

	addl %ecx, (%eax)
	;subl %edx, 4(%eax)
	;imull $16, (%eax, %edx, 4)
	;incl 8(%eax)
	;decl %ecx
	;subl %edx, %eax

	popl %ebp