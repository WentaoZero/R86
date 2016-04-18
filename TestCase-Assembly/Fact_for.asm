;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $5, 4(%ebp)
	;set n

;Fact_for:
	pushl %ebp
	movl %esp, %ebp

	movl 8(%ebp), %ecx
	movl $2, %edx
	movl $1, %eax
	cmpl $1, %ecx
	jle .L14

.L17:
	imull %edx, %eax
	addl $1, %edx
	cmpl %edx, %ecx
	jge .L17
.L14: