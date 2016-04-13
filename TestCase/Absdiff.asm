;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $27, 4(%ebp)
	;set x
	movl $3, 8(%ebp)
	;set y

;Absdiff:
	pushl %ebp
	movl %esp, %ebp

	movl 8(%ebp), %edx
	movl 12(%ebp),%eax
	cmpl %eax, %edx
	jge .L2
	subl %edx, %eax
	jmp .L3
.L2:
	subl %eax, %edx
	movl %edx, %eax
.L3: