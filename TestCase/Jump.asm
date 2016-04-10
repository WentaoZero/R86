;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16

;jump:
	movl $0, %eax
	jmp .L1
	movl -1, %edx
	;illegal access to memory
.L1:
	popl %edx