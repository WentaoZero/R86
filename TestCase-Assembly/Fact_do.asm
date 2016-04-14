;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $5, 4(%ebp)
	;set n

;Fact_do:
	pushl %ebp
	movl %esp, %ebp

	movl 8(%ebp), %edx
	movl $1, %eax

.L2:
	imull %edx, %eax
	subl $1, %edx
	cmpl $1, %edx
	jg .L2