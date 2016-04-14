;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $6, 4(%ebp)
	;set n

;Fact_while:
	pushl %ebp
	movl %esp, %ebp

	movl 8(%ebp), %edx
	movl $1, %eax
	cmpl $1, %edx
	jle .L7

.L10:
	imull %edx, %eax
	subl $1, %edx
	cmpl $1, %edx
	jg .L10

.L7: