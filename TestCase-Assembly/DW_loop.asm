;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $0, 4(%ebp)
	;set x
	movl $0, 8(%ebp)
	;set y
	movl $7, 12(%ebp)
	;set n

;dw_loop:
	pushl %ebp
	movl %esp, %ebp

	movl 8(%ebp), %eax
	movl 12(%ebp), %ecx
	movl 16(%ebp), %edx

.L2:
	addl %edx, %eax
	imull %edx, %ecx
	subl $1, %edx
	testl %edx, %edx
	jle .L5
	cmpl %edx, %ecx
	jl .L2
.L5: